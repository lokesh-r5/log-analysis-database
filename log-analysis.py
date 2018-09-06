#!/usr/bin/env python

import psycopg2


def connect(dbname="news"):
    """Connect to the PostgreSQL database and returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(dbname))
        c = db.cursor()
        return db, c
    except:
        print("Error in connecting to database")

def popular_articles(popular_articles_query):
    """Prints most popular three articles of all time"""
    db, c = connect()
    c.execute(popular_articles_query)
    result = c.fetchall()
    db.close()
    print "\nThe most popular three articles of all time:\n"
    for i in range(0, len(result), 1):
        print "\"" + result[i][0] + "\" - " + str(result[i][1]) + " views"

def popular_authors(popular_authors_query):
    """Prints most popular article authors of all time"""
    db, c = connect()
    c.execute(popular_authors_query)
    result = c.fetchall()
    db.close()
    print "\nThe most popular article authors of all time:\n"
    for i in range(0, len(result), 1):
        print "\"" + result[i][0] + "\" - " + str(result[i][1]) + " views"

def log_status(log_status_query):
    """Print days on which more than 1% of requests lead to errors"""
    db, c = connect()
    c.execute(log_status_query)
    result = c.fetchall()
    db.close()
    print "\nDays with more than 1% of errors:\n"
    for i in range(0, len(result), 1):
        print str(result[i][0])+ " - "+str(round(result[i][1]))+"% errors"


popular_articles_query = "SELECT ar.title AS title, COUNT(*) AS views FROM articles AS ar JOIN log AS l ON SUBSTRING(l.path, 10) = ar.slug GROUP BY ar.title ORDER BY views DESC"
popular_articles(popular_articles_query)
popular_authors_query = "SELECT au.name AS author, v.views AS views FROM authors AS au JOIN (SELECT ar.author AS author_id, COUNT(*) AS views FROM articles AS ar JOIN log AS l ON SUBSTRING(l.path, 10) = ar.slug GROUP BY ar.author) v ON v.author_id = au.id ORDER BY views DESC"
popular_authors(popular_authors_query)
log_status_query = "SELECT time::timestamp::date AS day, SUM(CASE WHEN status = '404 NOT FOUND' THEN 1 ELSE 0 END) * 100.0/count(*) AS percentage FROM log GROUP BY day HAVING SUM(CASE WHEN status = '404 NOT FOUND' THEN 1 ELSE 0 END) * 100.0/COUNT(*)>1.0"
log_status(log_status_query)
