from mg_app_framework import TaskKey, get_handler, get_logger, get_organization, get_store


async def create_collection_and_index(collection_name: str, indexs: list) -> None:
    '''

    :param collection_name:
    :param indexs: [("item_code", 1), ("order_code", 1)]
    :return:
    '''
    handle = get_handler(TaskKey.mongodb_async)
    app_name = get_store().get_data()['app_module_name']
    db_name = get_organization() + '_' + app_name
    db = handle[db_name]
    collection_names = await db.list_collection_names(False)
    if collection_name not in collection_names:
        collection_current = await db.create_collection(collection_name)
        for index in indexs:
            await collection_current.create_index([index])
            get_logger().info('create collection[%s] and index %s success', collection_name, index)


def get_collection_handle(database_name: str = '', collection_name: str = ''):
    handle = get_handler(TaskKey.mongodb_async)
    app_name = get_store().get_data()['app_module_name']
    db_name = database_name if database_name else get_organization() + '_' + app_name
    return handle[db_name].get_collection(collection_name)


async def count_total_num_of_mongodb(handle):
    '''
    统计mongodb中非'admin' 和'config'数据库以外的所有数据条数
    :param handle: 异步mongodb连接句柄
    :return:int
    '''

    database_list = await handle.list_database_names()
    total_num = 0
    for database in database_list:
        if database != 'admin' and database != 'config':
            collection_list = await handle[database].list_collection_names()
            for collection in collection_list:
                db = handle[database]
                n = await db[collection].count_documents({'_id': {'$exists': True}})
                total_num += n

    return total_num
