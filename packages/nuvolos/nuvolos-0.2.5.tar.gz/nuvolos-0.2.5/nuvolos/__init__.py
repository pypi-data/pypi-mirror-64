import os
import logging
from sqlalchemy import engine_from_config
from configparser import ConfigParser
import re

logger = logging.getLogger(__name__)


def get_dbpath():
    path_filename = os.getenv("ACLIB_DBPATH_FILE", "/lifecycle/.dbpath")
    if not os.path.exists(path_filename):
        logger.debug(f"Could not find dbpath file {path_filename}.")
        return None, None
    with open(path_filename, 'r') as path_file:
        lines = path_file.readlines()
        if len(lines) == 0:
            logger.debug(f"Could not parse dbpath file: {path_filename} is empty.")
            return None, None
        first_line = lines[0].rstrip()
        # Split at "." character
        # This should have resulted in two substrings
        split_arr = re.split("\".\"", first_line)
        if len(split_arr) != 2:
            logger.debug(
                f"Could not parse dbpath file: pattern \".\" not found in {path_filename}. Are the names escaped with double quotes?")
            return None, None
        # Split removes the two quotes
        db_name = split_arr[0] + "\""
        schema_name = "\"" + split_arr[1]
        logger.debug(f"Found database = {db_name}, schema = {schema_name} in dbpath file {path_filename}.")

        return db_name, schema_name


def get_url(username = None, password = None, dbname=None, schemaname=None):
    if username is None and password is None:
        username_filename = os.getenv("ACLIB_USERNAME_FILENAME", "/secrets/username")
        snowflake_access_token_filename = os.getenv("ACLIB_SNOWFLAKE_ACCESSS_TOKEN_FILENAME",  "/secrets/snowflake_access_token")
        if not os.path.exists(username_filename) or not os.path.exists(snowflake_access_token_filename):
            raise FileNotFoundError(f"It seems you are not in Nuvolos. Please provide both a username and password argument to this function. If you are in Nuvolos, please contact support.")
        else:
            with open(username_filename) as username, open(snowflake_access_token_filename) as access_token:
                cred_username = username.readline()
                cred_snowflake_access_token = access_token.readline()
            credd = {'username': cred_username}
            credd['snowflake_access_token'] = cred_snowflake_access_token
            snowflake_host = os.getenv("ACLIB_SNOWFLAKE_HOST", "alphacruncher.eu-central-1")
            url = 'snowflake://' + credd['username'] + ':' + credd[
                'snowflake_access_token'] + '@' + snowflake_host + '/?warehouse=' + credd['username']
            masked_url = 'snowflake://' + credd['username'] + ':********' + '@' + snowflake_host + '/?warehouse=' + credd[
                'username']
    elif username is not None and password is None:
        raise Exception("You have provided a username but not a password. Please either provide both arguments or leave both arguments empty.")
    elif username is None and password is not None:
        raise Exception("You have provided a password but not a username. Please either provide both arguments or leave both arguments empty.")
    else:
        credd = {'username': username}
        credd['snowflake_access_token'] = password
        snowflake_host = os.getenv("ACLIB_SNOWFLAKE_HOST", "alphacruncher.eu-central-1")
        url = 'snowflake://' + credd['username'] + ':' + \
                credd['snowflake_access_token'] + '@' + snowflake_host + '/?warehouse=' + credd['username']
        masked_url = 'snowflake://' + credd['username'] + ':' + \
                '********' + '@' + snowflake_host + '/?warehouse=' + credd['username']
    if dbname is None and schemaname is None:
        db_name, schema_name = get_dbpath()
    elif dbname is not None and schemaname is None:
        raise Exception("You have provided a dbname argument but not a schemaname argument. Please either provide both or provide none of them.")
    elif dbname is None and schemaname is not None:
        raise Exception("You have provided a schemaname argument but not a dbname argument. Please either provide both or provide none of them.")
    else:
        db_name = dbname
        schema_name = schemaname
    
    if db_name:
        url = url + '&database=' + db_name
        masked_url = masked_url + '&database=' + db_name
        if schema_name:
            url = url + '&schema=' + schema_name
            masked_url = masked_url + '&schema=' + schema_name
    logger.debug('Built SQLAlchemy URL: ' + masked_url)
    return url


def get_engine(username = None, password = None, dbname = None, schemaname = None):
    return engine_from_config({'sqlalchemy.url': get_url(username, password, dbname, schemaname), 'sqlalchemy.echo': False})

def get_connection(username = None, password = None, db_name = None, schema_name = None):
    loc_eng = get_engine(username, password, dbname, schemaname)
    return loc_eng.connect()
    
