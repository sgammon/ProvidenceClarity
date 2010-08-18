import os, sys, logging
import wsgiref.handlers

from google.appengine.ext import webapp

from ProvidenceClarity import pc_config
from ProvidenceClarity.handlers import util, input, output, workers, admin, api

from ProvidenceClarity.handlers.util import errors
from ProvidenceClarity.handlers.input import receiver, scraper
from ProvidenceClarity.handlers.admin import data
from ProvidenceClarity.handlers.workers import mail, xmpp, analyzer, data
from ProvidenceClarity.handlers.api import data as data_api

rp = pc_config.get('pc_url_prefix','handlers','/_pc')

ROUTES = [

    ## Admin Panel Handlers
    (rp+'/manage/*$',admin.IndexHandler),
    (rp+'/manage/data',admin.data.DataIndex),
    (rp+'/manage/data/(.+)/list',admin.data.DataList),
    (rp+'/manage/data/(.+)/create',admin.data.DataCreate),
    (rp+'/manage/data/(.+)/view/(.+)',admin.data.DataView),
    (rp+'/manage/data/(.+)/edit/(.+)',admin.data.DataEdit),    
    (rp+'/manage/data/(.+)/delete/(.+)',admin.data.DataDelete),

    ## Data API Handlers
    (rp+'/api/data/list', data_api.MasterTypeListHandler), # master types list
    (rp+'/api/data/query', data_api.MasterQueryHandler), # raw GQL query endpoint
    (rp+'/api/data/(.+)/list',data_api.TypeListHandler), # listing a type
    (rp+'/api/data/(.+)/delete',data_api.DeleteHandler), # deleting a record
    (rp+'/api/data/(.+)/update',data_api.UpdateHandler), # updating a record
    (rp+'/api/data/(.+)/create',data_api.CreateTypeHandler), # create a type record
    (rp+'/api/data/(.+)/query',data_api.QueryTypeHandler), # query a type
    (rp+'/api/data/entity/(.+)/create',data_api.CreateEntityHandler), # create an entity

    ## Outgoing Queue Workers
    (rp+'/worker/outgoing/mail',workers.mail.OutgoingMail),
    (rp+'/worker/outgoing/xmpp',workers.xmpp.OutgoingXMPP),
    
    ## Analyzer Queue Workers
    (rp+'/worker/analyzer/object',analyzer.ObjectAnalyzer),
    (rp+'/worker/analyzer/relation',analyzer.RelationAnalyzer),
    (rp+'/worker/analyzer/stat',analyzer.StatAnalyzer),
    (rp+'/worker/analyzer/mapreduce',analyzer.MapReduceAnalyzer),
    
    ## Data Queue Workers
    (rp+'/worker/data/transaction',data.TransactionWorker),
    (rp+'/worker/data/indexer',data.IndexWorker),
    (rp+'/worker/data/cacher',data.CacheWorker),
    (rp+'/worker/data/hygiene',data.HygieneWorker),
    (rp+'/worker/data/expiration',data.ExpirationWorker),
    (rp+'/worker/data/scheduler',data.SchedulerWorker),
    
    ## Input Handlers
    (rp+'/input/receiver/(.+)',receiver.ReceiverHandler),
    
    ## Incoming API Services
    (rp+'/_ah/xmpp/message/chat/',workers.mail.IncomingMail),
    (rp+'/_ah/mail/.+',workers.xmpp.IncomingXMPP),
    
    ## Generic Handlers
    (rp+'/error/404',util.errors.Error404),
    (rp+'/error/403',util.errors.Error403),    
    (rp+'/*$',util.IndexHandler)

]


def main():
    
    application = webapp.WSGIApplication(ROUTES, debug=pc_config.get('debug','handlers',False))
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()