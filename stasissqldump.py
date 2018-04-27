#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 2 -*-

# Check_mk plugin for stasis_sql_dump
# GPL (C) Lars Falk-Petersen <dev@falk-petersen.no>, 2014
#
# Check if a database server is running,
# and if so check that we have a valid backup.

stasissqldump_default_levels = (0, 100, 1)

def inventory_stasissqldump(info):
  #print info
  # [['Errors', '0'], ['Size', '23900'], ['New', '3'], ['dbserver', '...']]

  # Return defaults if data is bad.
  if len(info) < 4:
    return [(None, 'stasissqldump_default_levels')]

  #TODO: Make this work:
  #errors, size, new, dbserver = info
  #inventory.append( ('errors', errors[1]) )
  #inventory.append( ('size', size[1]) )
  #inventory.append( ('new', new[1]) )
  #return inventory
  return [(None, 'stasissqldump_default_levels')]


def check_stasissqldump(item, params, info):
  # unpack check parameters
  errorlevel, sizelevel, newlevel = params

  # Unpack statuses
  dbserver = ''
  for i in info[3]:
    if 'dbserver' == i:
      continue
    dbserver = dbserver + i  + ' '

  errors = int(info[0][1])
  size = int(info[1][1])
  new = int(info[2][1])

  # Perfdata
  perfdata = [ ( "size", size, 2000, 1000 ) ]

  # Check if a db server exists
  if 0 == len(dbserver):
    return (0, 'OK - No database server running.', perfdata)

  elif errors != int(errorlevel):
    # Errorlog exit codes:
    #   0 = No databases
    #  -1 = No config
    #  -2 = No errorlog set

    if -1 == errors:
      return (3, 'UNKNOWN - ' + dbserver , perfdata)
    elif -2 == errors:
      return (3, 'UNKNOWN - (code ' + str(errors) + '). ' + dbserver , perfdata)
    else:
      return (2, 'ERROR - Errors in Stasis SQL dump log file (' \
        + str(errors) + ' lines of errors). ' + dbserver , perfdata)

  elif size < int(sizelevel):
    return (1, 'WARNING - Stasis SQL dump size too small (' \
      + str(size) + ' kbytes). ' + dbserver, perfdata)

  elif new < int(newlevel):
    return (2, 'ERROR - Too few fresh Stasis SQL dumps (' \
      + str(new) + ' fresh files). ' + dbserver, perfdata)

  else:
    return (0, 'OK - Backup looks good (' + str(size) + ' kbytes, ' \
      + str(new) + ' fresh files). ' + dbserver, perfdata)


check_info['stasissqldump'] = (
  check_stasissqldump,
  'Stasis SQL Dump',
  1,
  inventory_stasissqldump
)

#TODO: This doesn't work:
# check_info['stasissqldump'] = {
#     'check_function':       check_stasissqldump,
#     'service_description':  "Stasis SQL Dump",
#     'has_perfdata':         False,
#     'inventory_function':   inventory_stasissqldump,
# }
