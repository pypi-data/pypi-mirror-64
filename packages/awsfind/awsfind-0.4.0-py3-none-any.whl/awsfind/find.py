#!/usr/bin/env python3
""" ifind - AWS Instance Finder

Searches across all accounts and regions for instances using chaim credentials

search accounts in alphabetical order
    ifind <instance-id> <instance-id> ... <instance-id>

to search accounts in random order (maybe quicker)
    ifind -r <instance-id> <instance-id> ... <instance-id>

"""
import random
import sys
import threading
import time
from awsfind import __version__
import ccalogging
import ccautils.utils as UT
from ccautils.errors import errorRaise
from ccautils.errors import errorExit
from chaim.chaimmodule import Chaim
from ccaaws.ec2 import EC2

ccalogging.setConsoleOut()
ccalogging.setInfo()
log = ccalogging.log


def getInstsAsList(insts):
    try:
        tmp = xinsts = []
        if type(insts) is str:
            if "," in insts:
                tmp = insts.split(",")
            else:
                tmp = insts.split(" ")
        elif type(insts) is list:
            tmp = insts
        for xt in tmp:
            xinsts.append(xt.strip())
        return xinsts
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def getInstanceInfo(inst):
    try:
        iname = ""
        iid = inst["InstanceId"]
        if "Tags" in inst:
            try:
                for tag in inst["Tags"]:
                    if tag["Key"] == "Name":
                        iname = tag["Value"]
            except KeyError as k:
                pass
        return (iid, iname)
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def findInRegion(xinsts, region, acctname, results, index):
    try:
        zinsts = []
        ec2 = EC2(region=region, profile="tempname")
        for inst in xinsts:
            # have to find 'em one by one, as
            # findInstances will return an empty list
            # if at least one of them is not found
            resp = ec2.findInstances([inst])
            if len(resp) > 0:
                zinsts.append(resp[0])
        res = []
        if len(zinsts) > 0:
            for inst in zinsts:
                iid, iname = getInstanceInfo(inst)
                if iname == "":
                    iname = "UNNAMED"
                res.append((iid, iname, region, acctname))
                # print(f"\r{acctname}: {region}: {iname}: {iid}")
        results[index] = res
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def removeIid(iid, xinsts):
    """ remove the iid from the list of instances"""
    try:
        log.debug("rebuilding instances list")
        nxinsts = []
        for xi in xinsts:
            log.debug(f"checking {xi} against {iid}")
            if xi != iid:
                log.debug(f"adding in {xi}")
                nxinsts.append(xi)
        return nxinsts
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def normaliseResults(nxresults):
    """ transforms results list of tuples into a dictionary"""
    try:
        results = {}
        acct = 3
        region = 2
        iname = 1
        iid = 0
        for res in nxresults:
            if res[acct] not in results:
                results[res[acct]] = {}
            if res[region] not in results[res[acct]]:
                results[res[acct]][res[region]] = []
            xd = {"iid": res[iid], "name": res[iname]}
            results[res[acct]][res[region]].append(xd)
        return results
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def checkResults(results, xinsts):
    try:
        nxinsts = xinsts
        nxresults = []
        for result in results:
            if len(result) > 0:
                for res in result:
                    nxresults.append(res)
                    log.debug(f"removing {result}")
                    iid = res[0]
                    nxinsts = removeIid(iid, nxinsts)
        log.debug(f"finding {len(xinsts)} instances, have {len(nxinsts)} to find")
        return (nxinsts, nxresults)
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def doThreads(acct, regions, xinsts):
    try:
        threads = []
        results = [() for x in regions]
        for ii in range(len(regions)):
            t = threading.Thread(
                target=findInRegion, args=[xinsts, regions[ii], acct[1], results, ii]
            )
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        nxinsts, nxresults = checkResults(results, xinsts)
        results = normaliseResults(nxresults)
        return (nxinsts, results)
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def doFindInst(xinsts, accts, regions):
    try:
        results = {}
        nxinsts = xinsts
        acn = len(accts) - 1
        rcn = len(regions)
        iicn = icn = xicn = len(nxinsts)
        cn = 0
        imsg = "instance" if iicn == 1 else "instances"
        print(f"Searching {acn} accounts in {rcn} regions for {iicn} {imsg}\n")
        for acct in accts:
            # chaim cannot obtain credentials for the billing account
            if acct[0] != "324919260230":
                with Chaim(acct[1], "rro", 1) as success:
                    if success:
                        cn += 1
                        print(
                            f"\r{cn:-3}/{acn:<4}{xicn:-3}/{iicn:<4} {acct[1]:<40}",
                            end="",
                        )
                        nxinsts, nxresults = doThreads(acct, regions, nxinsts)
                        xicn = len(nxinsts)
                        if xicn != icn:
                            for acctname in nxresults:
                                results[acctname] = nxresults[acctname]
                            icn = xicn
                            # if icn > 0 and icn == 1:
                            #     print(f"finding {nxinsts[0]}")
                            # elif icn > 1:
                            #     print(f"finding {icn} instances.")
            if icn == 0:
                break
        print()
        printResults(results)
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def printResults(results):
    """outputs the results to the console"""
    try:
        headings = ["Account", "Region", "Name", "Instance ID"]
        headline = (
            f"\n\n{headings[0]:<30}{headings[1]:<10}{headings[2]:<30}{headings[3]:<20}"
        )
        if len(results) > 0:
            print(headline)
            print("-" * 90)
            for account in results:
                for region in results[account]:
                    for inst in results[account][region]:
                        msg = f"{account:<30}"
                        msg += f"{region:<10}"
                        msg += f"""{inst["name"]:<30}"""
                        msg += f"""{inst["iid"]:<20}"""
                        print(msg)
            print("")
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def awsFindInstances():
    """ search all accounts for instances
    """
    try:
        print(f"ifind {__version__}")
        if len(sys.argv) == 1:
            log.warning("No instances supplied to find")
            usage()
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            usage()
        if sys.argv[1] == "-r":
            dorand = True
            insts = sys.argv[2:]
        else:
            dorand = False
            insts = sys.argv[1:]
        xinsts = getInstsAsList(insts)
        log.debug(f"finding {xinsts}")
        cn = len(xinsts)
        if cn > 0:
            log.debug("setting up ec2")
            ec2 = EC2()
            regions = ec2.getRegions()
            log.debug(f"{len(regions)} regions found")
            del ec2
            log.debug("setting up chaim")
            ch = Chaim("wibble", "wobble")
            accts = ch.requestList()
            if dorand:
                random.shuffle(accts)
            log.debug(f"{len(accts)} accounts found")
            del ch
            xstart = time.time()
            doFindInst(xinsts, accts, regions)
            xend = time.time()
            taken = UT.hms(int(xend - xstart), single=True)
            print(f"search took {taken}")
        else:
            log.warning("No instances supplied to find")
            usage()
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorExit(fname, e)


USAGE = f"{__doc__}"


def usage():
    sys.exit(USAGE)


if __name__ == "__main__":
    awsFindInstances()
