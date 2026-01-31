from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def create_entity(self, entity_name, parent=None):
        with self._driver.session() as session:
            if parent:
                result = session.write_transaction(self._create_entity_with_parent, entity_name, parent)
            else:
                result = session.write_transaction(self._create_entity, entity_name)
            return result

    @staticmethod
    def _create_entity(tx, entity_name):
        result = tx.run("CREATE (:事物 {名称: $名称}) RETURN $名称", 名称=entity_name)
        return result.single()[0]

    @staticmethod
    def _create_entity_with_parent(tx, entity_name, parent):
        result = tx.run("MATCH (p:事物 {名称: $parent_name}) "
                        "CREATE (p)-[:包含]->(:事物 {名称: $名称}) "
                        "RETURN $名称", parent_name=parent, 名称=entity_name)
        return result.single()[0]

# 连接到 Neo4j 数据库
uri = "bolt://localhost:7687"
user = "neo4j"
password = "k_Cr29KhMKTupRK"

connection = Neo4jConnection(uri, user, password)
connection.connect()

# 创建功能区分类体系的主要功能区实体
functional_classifications = [
    "体育与文化用地", "工业用地", "居住用地", "教育科研用地",
    "公园与绿地用地", "行政办公用地", "机场设施用地", "商业服务用地",
    "交通场站用地", "医疗卫生用地", "商务办公用地"
]

for classification in functional_classifications:
    connection.create_entity(classification, parent="功能区分类体系")

# 定义 POI 实体及其所属的功能区
poi_to_functional_area = {
    "商业服务用地": ["餐饮", "大厦", "大型购物广场", "购物","休闲娱乐"],
    "交通场站用地": ["加油站", "汽车服务", "停车场"],
    "行政办公用地": ["政府机关", "公安交警"],
    "居住用地": ["居民小区点", "居委会点", "住宿"],
    "教育科研用地": ["科研教育"],
    "医疗卫生用地": ["医疗服务"],
    "体育与文化用地": ["操场", "体育场区域", "体育中心区域", "网球场区域", "运动场跑道"],
    "工业用地": ["工业区", "采石场区"],
    "公园与绿地用地": ["绿地", "绿色区域", "森林", "沙滩"],
    "机场设施用地": ["机场设施用地"],
    "商务办公用地":["金融服务"]

}

# 创建 POI 实体并将其连接到相应的功能区实体
for functional_area, pois in poi_to_functional_area.items():
    for poi in pois:
        connection.create_entity(poi, parent=functional_area)

print("指定的 POI 实体创建并关联成功.")

# 关闭连接
connection.close()
