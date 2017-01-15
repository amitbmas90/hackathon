#!/usr/bin/python

import boto3
import sys
import json
import urllib
import math
import requests

class Skypher():

    def __init__(self, group):
        """Intializing the Class by loading josn data"""
        self.group_data=group
        self.graphite=group.get("graphite")

    def sys_metrics(self):
        """Take each metrics and passthrough those to get the parameters"""
        for metrics in self.group_data.get('system_metric',None):

            status=self.check_sys_metric(self.group_data.get(metrics).get('threshold'),
                                         self.group_data.get(metrics).get('graphite_url'),
                                         self.group_data.get(metrics).get('thereafter'))
            status = 2
            if status == 1 :
                self.scale(self.scale_up)
            if status == 2:
                self.predict(self.group_data.get('holt_numBox'),self.group_data.get('numBox'))
            if status == 3:
                now = datetime.datetime.now()
                if  not now.minute % 10:

                    self.scale()

    def scale(self, num):
        url="{}{}".format(self.group_data.get('scale'),num)
        print url
        data=requests.get(url)
        print data

    def health_metrics(self):
        all = self.group_data
        health=self.check_health(all.get('dr_metric').get('health_check'),
                                all.get('dr_metric').get('response'),
                                all.get('dr_metric').get('timeout'))


    def predict(self,holt_graphite_url,graphite_url):

        complete_url = "{}?target={}".format(self.graphite, holt_graphite_url)
        data = self.pull_graphite_data(complete_url)
        predicted_numbox=int(max(data[:-5]))
        complete_url = "{}?target={}".format(self.graphite, graphite_url)
        data = self.pull_graphite_data(complete_url)
        current_numbox=int(data[-1])
        if predicted_numbox> current_numbox:
            print "scaling up"
            self.scale(predicted_numbox)

    def check_sys_metric(self, threshold, graphite_url, thereafter):

        complete_url="{}?target={}".format(self.graphite,graphite_url)
        print complete_url
        data=self.pull_graphite_data(complete_url)
        percentage, scale = [ int(x) for x in thereafter.split(':')]
        print percentage, scale
        if data[-1] <= 40:
            check_ratio = math.ceil(40 - data[-1])
            scale_up = check_ratio/percentage*scale
            if scale_up >1 :
                self.scale_up=scale_up
                return 1
        if 40 <= data[-1] <= 60:
            return 2
        if data[-1] >=80:
            return 3
        else:
            return 0



    def check_health(self, health_check, response, timeout):

        counter = 0
        while counter <5:
          try:
               r2 = requests.get(health_check, timeout=timeout, auth=HTTPBasicAuth('guest', 'guest'))
          except requests.exceptions.RequestException as e:
               sys.stderr.write("%s: %s\n" % (health_check, e))
               counter+=1
               continue
          if r2.status_code != response:
               counter+=1
               continue
          elif(r2.status_code == response):
               print "Health check: OK  {}".format(health_check)
               return 0
        if counter == 5:
            print "scale up colo2 and shift traffic"

    def pull_graphite_data(self, url):
        """Pull down raw data from Graphite"""
        # Make sure the url ends with '&rawData'
        if not url.endswith('&rawData'):
            url = url + '&rawData'
        print url
        # Catch URL errors
        try:

            data = urllib.urlopen(url).read().strip()
            #d1=requests.get(url, auth=HTTPBasicAuth('guest', 'guest'))
            #print d1
            #data=d1.text.strip()
            print data
            if len(data) == 0:
                sys.stderr.write("Error: No data was returned. Did you specify an existing metric? - %s" % url)
                return 0
            all_data_points = data.split('|')[-1].split(',')
            data_set = [float(x) for x in all_data_points
                        if not x.startswith("None")]
            return data_set
        except Exception, e:
            sys.stderr.write("%s: Unable to open URL\nError: %s" % url, str(e))
            return 0




#    def check_thresholds(self, data):

def parse_json(filename):

    with open(filename, "r") as infile:
        data = json.load(infile)
    return data


if __name__ == "__main__":

    data = parse_json('./dat.json')
    if not data.get("groups",None):
        sys.stderr.write("%s: No valid groups found\n" % data)
    for group in data.get("groups",None):
        print group
        if group.get("name",None) == 'nginx-test-1':
            new = Skypher(group)
            new.sys_metrics()



