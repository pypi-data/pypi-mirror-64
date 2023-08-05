#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import re
import json
from collections import OrderedDict, Counter
from datetime import datetime
import logging

from .. import VISTA_DATA_BASE_DIR
from ..cacher.cacherUtils import FMQLReplyStore, FilteredResultIterator, BASE_LOCN_TEMPL, DATA_LOCN_TEMPL, metaOfVistA
from .reduceType import TypeReducer, SubTypeReducer, DEFAULT_FORCE_COUNT_PTER_TYPES, validDayDT
from .reportReductions import reportReductions
from .DEFAULT_TYPE_CONFIGS import TYPE_CONFIGS

TYPER_LOCN_TEMPL = BASE_LOCN_TEMPL + "Typer/"
TYPER_REDUCTIONS_LOCN_TEMPL = TYPER_LOCN_TEMPL + "Reductions/"
TYPER_REPORTS_LOCN_TEMPL = TYPER_LOCN_TEMPL + "Reports/"

"""
As command, fmqltyper

Same pattern as v2er, cacher, using 
- [a] /data/vista/{STATIONNO}/... locations for reductions and reports and 
- [b] taking a configuration from the location the runtime runs from. 
- [c] that 'local' location is usually just a place for these configurations
- [d] onAndAfterDay/upToDay rely on create property and if set, want a "reductionLabel" to differentiate them
      IMPORTANT: replyWalkEfficiencyOff set when 'createProp' ie/ date order property
      doesn't match IEN order. In this case, you have to walk all entries and can't just
      skip up to the first in the date range and go from there (ex/ for appt in scheduling)

Supports 'countDateType' [YEAR|MONTH|WEEK|DAY] which decides the granularity of a date
counting.

REWRITE: proper per type settings for all with { typ: {setting1: ...} as opposed to
some globals like onAndAfterDay and then per setting, by type dictionaries. The current
way is too mixed up.

TODO:
- try yaml config https://pyyaml.org/wiki/PyYAMLDocumentation as can embed code 
easily ie/ include custom filters/enhancers inline so no need for custom ie/ can't
now invoke dynamically in command line
- for now, using print, not logging. May move over to one pattern 
"""
def reduceReportTypes(
        stationNumber, 
        types, 
        dataLocnTempl, 

        annotations = {},
        reductionLabel="",

        forceRedo=True, 
     
        onAndAfterDay="", 
        upToDay="", 
        countDateType="YEAR", 
    
        # By Type
        createDate={}, 
        subTypeProps={}, 
        forceCountPointerTypesExtra={}, 
        forceCountProperties={}, 
        replyWalkEfficiencyOff={},
        customEnhancers={}
    ):

    start = datetime.now()
    
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)    
    ch = logging.StreamHandler(sys.stdout)
    format = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(format)
    log.addHandler(ch)
    
    # Used to ensure 
    def ensureLocation(locn):
        if not os.path.isdir(locn):
            os.mkdir(locn)
        return locn
    ensureLocation(TYPER_LOCN_TEMPL.format(stationNumber))
    ensureLocation(TYPER_REDUCTIONS_LOCN_TEMPL.format(stationNumber))
    ensureLocation(TYPER_REPORTS_LOCN_TEMPL.format(stationNumber))
                    
    typesAndDates = dict((typId, createDate[typId] if typId in createDate else "") for typId in types)
    
    if onAndAfterDay:
        if not validDayDT(onAndAfterDay):
            raise Exception("Invalid 'on and after day': {}".format(onAndAfterDay))

    if upToDay:
        if not validDayDT(upToDay):
            raise Exception("Invalid 'up to day': {}".format(upToDay))
            
    if (upToDay or onAndAfterDay) and reductionLabel == "":
        raise Exception("You must name the reduction ('reductionLabel') for time limited ('onAndAfterDay'/'upToDay') reductions")
        
    if countDateType and countDateType not in ["YEAR", "MONTH", "WEEK", "DAY"]:
        raise Exception("'countDateType' must be YEAR | MONTH | WEEK | DAY")
        
    if reductionLabel == "":
        logging.info("About to reduce (and report) on {} types, starting at {} [PID {}]".format(len(typesAndDates), start, os.getpid()))
    else:
        logging.info("About to reduce (and report) on {} types, starting at {} [PID {}] - {} for onAndAfterDay {}, upToDay {}".format(len(typesAndDates), start, os.getpid(), reductionLabel, onAndAfterDay if onAndAfterDay else "-", upToDay if upToDay else "")) 
        
    def getCreateDay(resource, createDateProp):
        value = resource[createDateProp]["value"] if "value" in resource[createDateProp] else resource[createDateProp]["label"]
        dayValue = value.split("T")[0] # using lex comp on ISO‑8601 form as fastest
        if not validDayDT(dayValue):
            log.debug("Can't get create day as its date has invalid value: {}".format(dayValue))
            return None
        return dayValue      

    count = 0 # allow for 0 - no i defined
    filtered = 0      
    dataLocn = dataLocnTempl.format(stationNumber)  
    for i, typId in enumerate(sorted(typesAndDates, key=lambda x: float(re.sub(r'\_', '.', x))), 1):
        startTyp = start if len(types) == 1 else datetime.now()
            
        reductionLocn = ensureLocation(TYPER_REDUCTIONS_LOCN_TEMPL.format(stationNumber))
        redFFL = "{}/{}{}Reduction.json".format(reductionLocn, typId, reductionLabel)
        
        if forceRedo == False and os.path.isfile(redFFL):
            logging.info("Not reducing (and reporting) {} as already exists and NOT forceredo".format(typId))
            continue

        logging.info("Reducing (and reporting) {}".format(typId))
        
        startAtReply = ""
        efficientWalked = False
        if onAndAfterDay:
            if typ in replyWalkEfficiencyOff:
                logging.debug("No Start Efficiency: starting with first Reply and ignoring onAndAfterDay for skipping as either [1] walking reformed (RF) data which is usually from out of order multiples or [2] forced to walk all as property for onAndAfterDay is not create property (one in IEN order) ex/ appt start time")
            else:
                store = FMQLReplyStore(dataLocn)
                startAtReply = store.firstReplyFileOnOrAfterCreateDay(typId, typesAndDates[typId], onAndAfterDay)
                if startAtReply == "":
                    logging.info("** Exiting: can't find Reply to start at on and after day {}, create property {}".format(onAndAfterDay, typesAndDates[typId]))
                    break
                logging.debug("Start Efficiency: configuring Iterator for on and after time: on or after day {}, create property {}, starting at reply {}".format(onAndAfterDay, typesAndDates[typId], startAtReply))
                efficientWalked = True
        resourceIter = FilteredResultIterator(dataLocn, typId, isOrdered=False, startAtReply=startAtReply)
        fcpts = DEFAULT_FORCE_COUNT_PTER_TYPES
        if typId in forceCountPointerTypesExtra:
            fcpts.extend(forceCountPointerTypesExtra[typId])
        fcps = forceCountProperties[typId] if typId in forceCountProperties else []
        if typId in subTypeProps: 
            if isinstance(subTypeProps[typId], list):
                stps = subTypeProps[typId]
            else:
                stps = [subTypeProps[typId]]
            logging.info("Subtyping by '{}'".format("-".join(stps)))
            rtr = SubTypeReducer(typId, createDateProp=typesAndDates[typId], subTypeProps=stps, forceCountPointerTypes=fcpts, forceCountProperties=fcps, countDateType=countDateType)
        else:
            rtr = TypeReducer(typId, createDateProp=typesAndDates[typId], forceCountPointerTypes=fcpts, forceCountProperties=fcps, countDateType=countDateType)
        customEnhancer = None
        if typId in customEnhancers:
            customEnhancer = customEnhancers[typId]
            
        msgThres = 50000 
        upToDayStopped = False 
        filtered = Counter()  
        for i, resource in enumerate(resourceIter, 1):
            count += 1
            filteredSoFar = sum(filtered[c] for c in filtered)
            if i % msgThres == 0:
                logging.debug("Checked {} more resources for total of {:,}, sub type reducers {:,}, so far filtered {:,}, now in reply {} - {}".format(msgThres, i, rtr.subTypeReducerCount(), filteredSoFar, resourceIter.currentReplyFile(), datetime.now() - start))
            idProp = "id" if "id" in resource else "_id"
            if customEnhancer:
                resource = customEnhancer.enhance(resource)
                if not resource:
                    filtered["CUSTOM"] += 1
                    continue
            # Allows for out of order too
            if onAndAfterDay or upToDay:
                if typesAndDates[typId] not in resource:
                    filtered["NOCREATEDATE"] += 1
                    continue
                createDay = getCreateDay(resource, typesAndDates[typId])
                if not createDay:
                    filtered["BADCREATEDATE"] += 1
                    continue
                if onAndAfterDay and createDay < onAndAfterDay:
                    filtered["LTONAFTER"] += 1
                    continue
                # Can't efficiently cut out as start for appt can go on (ie/ not ordered)
                if upToDay and createDay >= upToDay:
                    filtered["GTEUPTO"] += 1
                    continue 
            rtr.transform(resource)
            
        pattData = rtr.reductions()
        # Add more meta to ALL Reduction
        allReds = [typeData for typeData in pattData if "_subTypeId" not in typeData]
        if len(allReds) != 1:
            raise Exception("Internal Error - expected one and only one ALL reduction")
        allRed = allReds[0]
        allRed["_stationNumber"] = stationNumber
        if efficientWalked:
            allRed["_efficientWalked"] = True
        if reductionLabel:
            allRed["_label"] = reductionLabel
        if onAndAfterDay:
            allRed["_onAndAfterDay"] = onAndAfterDay
        if upToDay:
            allRed["_upToDay"] = upToDay
        for annotationType in annotations:
            allRed["_{}".format(annotationType)] = annotations[annotationType]
                            
        json.dump(pattData, open(redFFL, "w")) 
     
        reportLocn = ensureLocation(TYPER_REPORTS_LOCN_TEMPL.format(stationNumber))
        reportReductions(pattData, "{}/{}{}Report.txt".format(reportLocn, typId, reductionLabel))
        
        if len(filtered):
            filteredMU = "/".join(["{} [{}]".format(reason, filtered[reason]) for reason in filtered])
            logging.info("Finished after {:,} resources of {} in {} at {}, {:,} explicitly filtered with {}".format(count, typId, datetime.now() - startTyp, datetime.now(), sum(filtered[c] for c in filtered), filteredMU))
        else:
            logging.info("Finished after {:,} resources of {} in {} at {}".format(count, typId, datetime.now() - startTyp, datetime.now()))
            
    if len(types) > 1:
        logging.info("Finished {} types at {} in {}".format(len(types), datetime.now(), datetime.now() - start))
        
"""
Map YR\d, DAY\d, MTH\d to date range, reductionLabel and default count date type
"""
def fromPeriod(vistaCutDate, period):

    if period == "ALL":
        return "", "", "YEAR"

    vistaCutDateDT = datetime.strptime(vistaCutDate.split("T")[0], "%Y-%m-%d")
    lastDayDT = vistaCutDateDT - relativedelta(days=1)
    lastDay = datetime.strftime(lastDayDT, "%Y-%m-%d")
    
    countDateType
    
    relDelta = None
    for mtchRE, keyword, defaultCountDateType in [
        (r'YR(\d+)', "years", "YEAR"),
        (r'MTH(\d+)', "months", "MONTH"),
        (r'WK(\d+)', "weeks", "DAY"),
        (r'DAY(\d+)', "days", "DAY")
    ]:
        mtch = re.match(mtchRE, period)
        if mtch:
            args = { keyword: int(mthMatch.group(1)) }
            relDelta = relativedelta(**args)
            countDateType = defaultCountDateType
            break
    if not relDelta:
        raise Exception("Need valid period but {} isn't one".format(period))
        
    onAndAfterDayDT = vistaCutDateDT - relDelta
    onAndAfterDay = datetime.strftime(onAndAfterDayDT, "%Y-%m-%d")
    return onAndAfterDay, lastDay, countDateType
        
# ############################# Driver ####################################

"""
Simplest command-line case. The general case of multiple types in a "grand 
configuration" is still supported above - it is being kept as it may still
be the optimal way to reduce a set of types with their own period and other settings.
"""
def reduceReportOneType(stationNumber, typ, period="ALL", reductionLabelExplicit="", customEnhancers={}):
        
    meta = metaOfVistA(stationNumber) # for cut date and annotations

    # Config is made to allow a loaded configuration to override all defaults
    config = OrderedDict()
    
    if reductionLabelExplicit:
        config["reductionLabel"] = reductionLabelExplicit
    else:
        config["reductionLabel"] = "" if period == "ALL" else period
                    
    config["forcedRedo"] = True
    config["dataLocnTempl"] = DATA_LOCN_TEMPL if not ("isRF" in config and config["isRF"]) else DATARF_LOCN_TEMPL
    config["replyWalkEfficiencyOff"] = False if not ("isRF" in config and config["isRF"]) else True
    
    config["onAndAfterDay"], config["upToDay"], config["countDateType"] = fromPeriod(meta["cutDate"], period)

    if typ in TYPE_CONFIGS:
        for setting in TYPE_CONFIGS[typ]:
            config[setting] = TYPE_CONFIGS[typ][setting] 
    # For this specific type - can override all but SNO and typ itself
    if len(argv) == 5:
        overrideConfigName = argv[3].split(".")[0]
        if not os.path.isfile("{}.json".format(overrideConfigName)):
            print("No override config file {}.json - exiting".format(overrideConfigName))
            return
        overrideConfig = json.load(open("{}.json".format(overrideConfigName)), object_pairs_hook=OrderedDict)
        for setting in overrideConfig:
            config[setting] = overrideConfig[setting]  
       
    # This routine works for many types at a time - config above is for one typ - map      
    reduceReportTypes(
        
        stationNumber, 
        [typ],
        config["dataLocnTempl"],
        
        annotations = {"vistaName": meta["vistaName"], "vistaCutDate": meta["cutDate"]},
        reductionLabel=config["reductionLabel"],       
        
        forceRedo=config["forceRedo"],
                
        onAndAfterDay=config["onAndAfterDay"],
        upToDay=config["upToDay"],
        countDateType=config["countDateType"],
                        
        createDate=({typ: config["createDate"]} if "createDate" in config else {}), 
        subTypeProps=({typ: config["subTypeProps"]} if "subTypeProps" in config else {}),
        forceCountProperties=({typ: config["forceCountProperties"]} if "forceCountProperties" in config else {}), 
        forceCountPointerTypesExtra=({typ: config["forceCountPointerTypesExtra"]} if "forceCountPointerTypesExtra" in config else {}),
        replyWalkEfficiencyOff={typ: config["replyWalkEfficiencyOff"]},
        
        customEnhancers=customEnhancers
    )

def main():

    assert (
        (sys.version_info[0] == 2 and sys.version_info[1] >= 7) or
        (sys.version_info[0] == 3 and sys.version_info[1] >= 3)
    )
    
    if len(argv) < 3 or len(argv) > 5:
        print("need to specify station number, type, [period] and ['override config' file] ex/ 442 2 [ALL] [{overrideConfigConstants}.json] - exiting")
        return

    stationNumber = argv[1]
    if not re.match(r'\d{3}$', stationNumber):
        print("need three digit station number - exiting")
        return
    
    typ = argv[2]
    
    period = argv[3] if len(argv) >= 4 else "ALL"
    if not re.match(r'(ALL|YR|MTH|WK|DAY)', period):
        print("invalid period {} - exiting".format(period))
        return
    
    reduceReportOneType(stationNumber, typ, period)
        
if __name__ == "__main__":
    main()
    
