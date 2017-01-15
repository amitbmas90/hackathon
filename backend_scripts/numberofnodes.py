#!/usr/bin/python
import urllib2
def main():
     req = urllib2.Request('http://172.31.30.18:9001/numberofcontainers?service=nginx-test-4')
     response = urllib2.urlopen(req)
     the_page = response.read()
     return  "PUTVAL {}/smartalert/gauge interval={} N:{}".format('test',60, the_page)

if __name__=="__main__":
   print main()

