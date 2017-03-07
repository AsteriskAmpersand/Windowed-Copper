from multiprocessing import Process, Lock
import prefixspan as ps
import fileprocessor as fp
import time
import sys
import math
sys.setrecursionlimit(10000)

def analyze(infile, outfile, options):
    u_db = open(infile, 'r')
    s_db = fp.asciiFormater(u_db)
    options['threshold']=int(math.ceil(options['threshold']*len(s_db)))
    start = time.time()
    res = ps.prefixspan(s_db, options)
    end = time.time()
    out = open(outfile,'w')
    out.write("Options: "+str(options)+'\n')
    out.write("Patterns Found: " + str(len(res))+'\n')
    out.write("Time Taken: " + str(end - start)+'\n')
    for pat in sorted(res, key=lambda x: x[1]):
        out.write(str(pat)+'\n')
    out.close()
    return

if __name__ == '__main__':
    infile = 'C10T8S8I8.txt'
    base = 'Results'
    delta = 0.0005
    start = 0.001
    threadlist = []
    for ratio in (start+mult*delta for mult in range(6,9)):
        options = {'threshold' : ratio}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)

        options = {'threshold' : ratio, 'gap' : 2000}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)

        options = {'threshold' : ratio, 'gap' : 0}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)

        options = {'threshold' : ratio, 'gap' : 1}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)

        options = {'threshold' : ratio, 'gap' : 2}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)

        options = {'threshold' : ratio, 'window' : 1}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)

        options = {'threshold' : ratio, 'window' : 2}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)

        options = {'threshold' : ratio, 'window' : 3}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)

        options = {'threshold' : ratio, 'window' : 3, 'gap' : 0}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)

        options = {'threshold' : ratio, 'window' : 3, 'gap' : 1}
        outfile = base+ ''.join((str(opt[0])+str(options[opt]) for opt in options)) + '.txt'
        p = Process(target=analyze, args=(infile,outfile,options))
        p.start()
        threadlist.append(p)
        
        for thread in threadlist:
            thread.join()
