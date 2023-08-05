# Canvs Toolbox Package

### Date Formatting
"MM/DD/YY" 

## General
from canvs_toolbox import general as gen
- gen.consolidate_data(file_path, file_type='csv')

## API Tools

### Canvs TV
from canvs_toolbox.api import tv as tv
- tv.twitter_daily(api_key, data_mode, start_date, end_date)
- tv.twitter_emotional_authors(api_key, series_id, start_date, end_date)
- tv.airings_backfill(api_key, data_mode, start_date, end_date)
- tv.facebook_backfill(api_key, data_mode, start_date, end_date)

### Canvs Watch
from canvs_toolbox.api import watch as watch
- watch.post_backfill(api_key, data_mode, start_date, end_date)
- watch.series_backfill(api_key, data_mode, start_date, end_date)

### Canvs Social
from canvs_toolbox.api import social as social
- social.get_facebook_posts(api_key, fb_id, org_id, start_date, end_date, query_increment=None
- social.get_page_collection(api_key, org_id, start_date, end_date, fb_pages, query_increment=None)

## Analytics Tools
TBD