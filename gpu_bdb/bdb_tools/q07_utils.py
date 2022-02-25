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

    item_cols = ["i_item_sk", "i_current_price", "i_category"]
    store_sales_cols = ["ss_item_sk", "ss_customer_sk", "ss_sold_date_sk"]
    date_cols = ["d_date_sk", "d_year", "d_moy"]
    customer_cols = ["c_customer_sk", "c_current_addr_sk"]
    customer_address_cols = ["ca_address_sk", "ca_state"]

    item_df = table_reader.read("item", relevant_cols=item_cols)
    store_sales_df = table_reader.read("store_sales", relevant_cols=store_sales_cols)
    date_dim_df = table_reader.read("date_dim", relevant_cols=date_cols)
    customer_df = table_reader.read("customer", relevant_cols=customer_cols)
    customer_address_df = table_reader.read(
        "customer_address", relevant_cols=customer_address_cols
    )

    if c:
        c.create_table("item", item_df, persist=False)
        c.create_table("customer", customer_df, persist=False)
        c.create_table("store_sales", store_sales_df, persist=False)
        c.create_table("date_dim", date_dim_df, persist=False)
        c.create_table("customer_address", customer_address_df, persist=False)

    return (
        item_df,
        store_sales_df,
        date_dim_df,
        customer_df,
        customer_address_df,
    )


