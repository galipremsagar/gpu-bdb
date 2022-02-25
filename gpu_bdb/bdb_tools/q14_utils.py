#
# Copyright (c) 2019-2022, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from bdb_tools.readers import build_reader

def read_tables(config, c=None):
    table_reader = build_reader(
        data_format=config["file_format"],
        basepath=config["data_dir"],
        split_row_groups=config["split_row_groups"],
        backend=config["backend"],
    )

    ws_columns = ["ws_ship_hdemo_sk", "ws_web_page_sk", "ws_sold_time_sk"]
    web_sales = table_reader.read("web_sales", relevant_cols=ws_columns)

    hd_columns = ["hd_demo_sk", "hd_dep_count"]
    household_demographics = table_reader.read(
        "household_demographics", relevant_cols=hd_columns
    )

    wp_columns = ["wp_web_page_sk", "wp_char_count"]
    web_page = table_reader.read("web_page", relevant_cols=wp_columns)

    td_columns = ["t_time_sk", "t_hour"]
    time_dim = table_reader.read("time_dim", relevant_cols=td_columns)

    if c:
        c.create_table("household_demographics", household_demographics, persist=False)
        c.create_table("web_page", web_page, persist=False)
        c.create_table("web_sales", web_sales, persist=False)
        c.create_table("time_dim", time_dim, persist=False)

    return (web_sales, household_demographics, web_page, time_dim)

