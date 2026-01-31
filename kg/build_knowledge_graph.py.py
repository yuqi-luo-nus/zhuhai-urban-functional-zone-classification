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

    def clear_database(self):
        with self._driver.session() as session:
            session.write_transaction(self._clear_database)

    @staticmethod
    def _clear_database(tx):
        tx.run("MATCH (n) DETACH DELETE n")

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
uri = "bolt://localhost:7687"  # Neo4j 服务器地址
user = "neo4j"  # Neo4j 用户名
password = "k_Cr29KhMKTupRK"  # Neo4j 密码

connection = Neo4jConnection(uri, user, password)
connection.connect()

# 清空数据库
connection.clear_database()

# 创建实体
thing_entity = connection.create_entity("事物")

# 在事物实体下创建子实体
remote_sensing_entity = connection.create_entity("遥感产品", parent="事物")
grid_entity = connection.create_entity("网格", parent="事物")
functional_classification_entity = connection.create_entity("功能区分类体系", parent="事物")

# 在遥感产品实体下创建子实体
guangpu = connection.create_entity("光谱特征", parent="遥感产品")
tuopu = connection.create_entity("拓扑", parent="遥感产品")
wenli = connection.create_entity("纹理特征", parent="遥感产品")

#光谱
fanshe = connection.create_entity("反射率", parent="光谱特征")
boduan = connection.create_entity("波段", parent="光谱特征")

#波段
nir=connection.create_entity("近红外", parent="波段")
red=connection.create_entity("红光", parent="波段")
green=connection.create_entity("绿光", parent="波段")
blue=connection.create_entity("蓝光", parent="波段")

# 在网格实体下创建子实体
longitude_latitude_entity = connection.create_entity("经纬网", parent="网格")
national_division_entity = connection.create_entity("国家区划", parent="网格")

# 在国家区划实体下创建子实体
country_entity = connection.create_entity("国家", parent="国家区划")

# 在国家实体下创建子实体
province_entity = connection.create_entity("省", parent="国家")

# 在省实体下创建子实体
city_entity = connection.create_entity("市", parent="省")

# 在市实体下创建子实体
district_entity = connection.create_entity("区", parent="市")

# 在区实体下创建子实体
street_entity = connection.create_entity("街道", parent="区")

# 在功能区分类体系下创建子实体
poi = connection.create_entity("POI", parent="功能区分类体系")
shuju = connection.create_entity("数据", parent="功能区分类体系")

#数据
renkou= connection.create_entity("人口密度", parent="数据")
tudi= connection.create_entity("土地开发强度", parent="数据")
jiaotong= connection.create_entity("交通流量", parent="数据")
qiye= connection.create_entity("企业密度", parent="数据")
#poi
water_entity = connection.create_entity("水域", parent="POI")
green_space_entity = connection.create_entity("绿地", parent="POI")
commerce_and_service_area_entity = connection.create_entity("商业和服务区", parent="POI")
residential_area_entity = connection.create_entity("住宅区", parent="POI")
road_and_transport_facility_entity = connection.create_entity("道路和交通设施", parent="POI")
public_administration_and_service_area_entity = connection.create_entity("公共管理和服务区", parent="POI")

# 在公共管理和服务区实体下创建子实体
government_agency_entity = connection.create_entity("政府机关", parent="公共管理和服务区")
administrative_unit_entity = connection.create_entity("行政单位", parent="公共管理和服务区")
higher_education_institution_entity = connection.create_entity("高等教育机构", parent="公共管理和服务区")
primary_school_entity = connection.create_entity("小学", parent="公共管理和服务区")
middle_school_entity = connection.create_entity("中学", parent="公共管理和服务区")
exhibition_hall_entity = connection.create_entity("图书馆", parent="公共管理和服务区")
exhibition_center_entity = connection.create_entity("展览馆", parent="公共管理和服务区")
sports_hall_entity = connection.create_entity("体育馆", parent="公共管理和服务区")
hospital_entity = connection.create_entity("医院", parent="公共管理和服务区")
# 在住宅区实体下创建子实体
real_estate_entity = connection.create_entity("房地产", parent="住宅区")
community_housing_entity = connection.create_entity("社区住房", parent="住宅区")
# 在道路和交通设施实体下创建子实体
parking_lot_entity = connection.create_entity("停车场", parent="道路和交通设施")
driving_school_entity = connection.create_entity("驾校", parent="道路和交通设施")
train_station_entity = connection.create_entity("火车站", parent="道路和交通设施")
subway_station_entity = connection.create_entity("地铁站", parent="道路和交通设施")
bus_station_entity = connection.create_entity("汽车站", parent="道路和交通设施")
ship_station_entity = connection.create_entity("码头", parent="道路和交通设施")

#商业
business=connection.create_entity("公司", parent="商业和服务区")
f=connection.create_entity("饭店", parent="商业和服务区")
s=connection.create_entity("商场", parent="商业和服务区")
b=connection.create_entity("酒店", parent="商业和服务区")
print("实体创建成功.")

# 关闭连接
connection.close()
