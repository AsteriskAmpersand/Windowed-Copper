from multiprocessing import Process, Lock
import prefixspan as ps
import fileprocessor as fp
import time
import sys
import math
sys.setrecursionlimit(10000)

def analyze(infile, outfile, options):
    u_db = open(infile, 'r')
    s_db, inttovar = fp.csvReader(u_db)
    options['threshold']=int(options['threshold'])
    start = time.time()
    res = ps.prefixspan(s_db, options)
    end = time.time()
    out = open(outfile,'w')
    out.write("Options: "+str(options)+'\n')
    out.write("Patterns Found: " + str(len(res))+'\n')
    out.write("Time Taken: " + str(end - start)+'\n')
    for pat in sorted(res, key=lambda x: x[1]):
        out.write(str(pat)+'\n') #[0].extended_representation(lambda x: inttovar[x]).replace(' ','').replace('><', '><').replace('\xe2\x89\xa5','>=')+' '+str(pat[1])
    out.close()
    return

if __name__ == '__main__':
    infile = 'D:\AsteriskAmpersand\Documents\GitHub\Windowed-Copper\TestFiles\DiscEpiData.csv'
    base = 'Results'
    delta = 1
    start = 11
    threadlist = []
    ###########################################################################################
    options = {'threshold' : 12}
    outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
    analyze(infile, outfile, options)
    #p = Process(target=analyze, args=(infile,outfile,options))
    #p.start()   
    #threadlist.append(p)
    
    options = {'threshold' : 12, 'window':200000}
    outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
    analyze(infile, outfile, options)
    #p = Process(target=analyze, args=(infile,outfile,options))
    #p.start()
    #threadlist.append(p)

    options = {'threshold' : 12, 'gap':200000}
    outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
    analyze(infile, outfile, options)
    #p = Process(target=analyze, args=(infile,outfile,options))
    #p.start()
    #threadlist.append(p)

    options = {'threshold' : 12, 'window':200000, 'gap':200000}
    outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
    analyze(infile, outfile, options)
    #p = Process(target=analyze, args=(infile,outfile,options))
    #p.start()
    #threadlist.append(p)
    ###########################################################################################
    
##    for ratio in (start+mult*delta for mult in range(0,8)):        
##        options = {'threshold' : ratio, 'maxSize' : 6}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##
##        options = {'threshold' : ratio, 'gap' : 6}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##
##        options = {'threshold' : ratio, 'gap' : 0}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##
##        options = {'threshold' : ratio, 'gap' : 1}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##
##        options = {'threshold' : ratio, 'gap' : 2}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##        
##        options = {'threshold' : ratio, 'window' : 3}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##
##        options = {'threshold' : ratio, 'window' : 4}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##
##        options = {'threshold' : ratio, 'window' : 5}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##
##        options = {'threshold' : ratio, 'window' : 4, 'gap' : 1}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##
##        options = {'threshold' : ratio, 'window' : 6, 'gap' : 3}
##        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
##        analyze(infile, outfile, options)
##        #p = Process(target=analyze, args=(infile,outfile,options))
##        #p.start()
##        #threadlist.append(p)
##       
##        for thread in threadlist:
##            thread.join()
