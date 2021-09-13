import json
import ConnOper

class CEntityai_target:
    '''
    ai_target表实体类
    '''
    def __init__(self):
        # 序号:1  # 列名:at_id  # 注释:序号  # 类型:int4  # 长度:32  # 是否NULL:True  # 小数点:0  # 是否主键:True
        self.at_id = None
        # 序号:2  # 列名:name  # 注释:目标名称  # 类型:varchar  # 长度:255  # 是否NULL:False  # 小数点:None  # 是否主键:False
        self.name = None
        # 序号:3  # 列名:tt_id  # 注释:目标类别ID对应bs_target_type  # 类型:int4  # 长度:32  # 是否NULL:True  # 小数点:0  # 是否主键:False
        self.tt_id = None
        # 序号:4  # 列名:category_id  # 注释:目标种类ID  # 类型:int4  # 长度:32  # 是否NULL:False  # 小数点:0  # 是否主键:False
        self.category_id = None
        # 序号:5  # 列名:shape_id  # 注释:目标形状ID  # 类型:int4  # 长度:32  # 是否NULL:False  # 小数点:0  # 是否主键:False
        self.shape_id = None
        # 序号:6  # 列名:shape_length  # 注释:目标尺寸-长(米)  # 类型:float4  # 长度:24  # 是否NULL:False  # 小数点:None  # 是否主键:False
        self.shape_length = None
        # 序号:7  # 列名:shape_width  # 注释:目标尺寸-宽(米)  # 类型:float4  # 长度:24  # 是否NULL:False  # 小数点:None  # 是否主键:False
        self.shape_width = None
        # 序号:8  # 列名:shape_height  # 注释:目标尺寸-高(米)  # 类型:float4  # 长度:24  # 是否NULL:False  # 小数点:None  # 是否主键:False
        self.shape_height = None
        # 序号:9  # 列名:position_relation_id  # 注释:位置关系ID  # 类型:int4  # 长度:32  # 是否NULL:False  # 小数点:0  # 是否主键:False
        self.position_relation_id = None
        # 序号:10  # 列名:bs_mid  # 注释:材质ID  # 类型:int4  # 长度:32  # 是否NULL:False  # 小数点:0  # 是否主键:False
        self.bs_mid = None

    @staticmethod
    def GetList(nPage=1, nSize=10):
        """获取ai_target列表

        Args:
            nPage (int, optional): 要返回的页码. Defaults to 1.
            nSize (int, optional): 每页记录条数. Defaults to 10.

        Returns:
            page (int): 页码
            size (int): 每页大小
            total (int): 数据总数
            list (list): 数据列表
            lstMissile (list): 弹药列表
        """        
        strSql = '''SELECT
            at_id,
            name,
            tt_id,
            category_id,
            shape_id,
            shape_length,
            shape_width,
            shape_height,
            position_relation_id,
            bs_mid
        FROM
            ai_target 
        ORDER BY at_id DESC
        LIMIT %s OFFSET %s'''

        nOffset = (nPage - 1) * nSize
        strSqlCount = '''SELECT COUNT(1) From ai_target'''

        lst, nTotal = ConnOper.ExeGetListAndCount(strSql, (nSize, nOffset), strSqlCount)

        lstMessage = []
        lstIds = []

        for r in lst:
            dict = {
                'at_id': r[0],
                'name': r[1],
                'tt_id': r[2],
                'category_id': r[3],
                'shape_id': r[4],
                'shape_length': r[5],
                'shape_width': r[6],
                'shape_height': r[7],
                'position_relation_id': r[8],
                'bs_mid': r[9]
            }
            lstIds.append(str(r[0]))	
            lstMessage.append(dict)

        if nTotal == 0:
            return {
                "page": nPage,
                "size": nSize,
                "total": nTotal,
                "list": lstMessage,
                "lstMissile":[]
            }
        
        #查询弹型
        strIds = ','.join(lstIds)
        '''获取ai_damage_strength列表'''
        
        strSqlSelMissile = f'''
        SELECT
            t_id,
            m_id 
        FROM
            ai_damage_strength 
        WHERE
            t_id IN ({strIds}) 
        ORDER BY
            t_id'''
        
        lstM = ConnOper.ExeGetList(strSqlSelMissile)
        lstMissile = []
        for r in lstM:
            dict = {
                't_id': r[0],
                'm_id': r[1]
            }
            lstMissile.append(dict)

        return {
            "page": nPage,
            "size": nSize,
            "total": nTotal,
            "list": lstMessage,
            "lstMissile":lstMissile
        }

    @staticmethod
    def GetListByFilter(dictProps: dict, nPage=1, nSize=10):
        """根据条件取得列表

        Args:
            dictProps (dict): 条件字典
            nPage (int, optional): 页码. Defaults to 1.
            nSize (int, optional): 每页大小. Defaults to 10.

        Returns:
            page (int): 页码
            size (int): 每页大小
            total (int): 总共多少条数据
            list (list): 数据列表
            lstMissile (list): 弹药列表
        """                
        strSql = '''
        SELECT
            at_id,
            name,
            tt_id,
            category_id,
            shape_id,
            shape_length,
            shape_width,
            shape_height,
            position_relation_id,
            bs_mid
        FROM
            ai_target
        '''

        strSqlCount = '''SELECT COUNT(1) From ai_target'''

        # if dictProps['name']:



        # 过滤条件语句数组 
        lstCriteriaSQL = []

        for prop in dictProps:
            if dictProps[prop]:
                if prop == 'name':
                    sql = "name like %s"
                else:
                    sql = f'''{prop} = {dictProps[prop]}'''
                lstCriteriaSQL.append(sql)

        # 过滤条件SQL语句
        strCriteriaSQL = ''
        for idx,s in enumerate(lstCriteriaSQL):
            if idx == 0:
                strCriteriaSQL += ' WHERE '
            else:
                strCriteriaSQL += ' AND '
            
            strCriteriaSQL += s
        
        

        strSql += strCriteriaSQL
        strSqlCount += strCriteriaSQL

        strSql += ''' ORDER BY 
        at_id DESC
        LIMIT %s OFFSET %s'''

        nOffset = (nPage - 1) * nSize
        
        lstIds = []

        print(strSql)

        if dictProps['name']:
            strLikeName = '%'+dictProps['name']+'%'
            lst, nTotal = ConnOper.ExeGetListAndCount(strSql, (strLikeName, nSize, nOffset), strSqlCount, (strLikeName,))
        else:
            lst, nTotal = ConnOper.ExeGetListAndCount(strSql, (nSize, nOffset), strSqlCount)

        lstMessage = []

        for r in lst:
            dict = {
                'at_id': r[0],
                'name': r[1],
                'tt_id': r[2],
                'category_id': r[3],
                'shape_id': r[4],
                'shape_length': r[5],
                'shape_width': r[6],
                'shape_height': r[7],
                'position_relation_id': r[8],
                'bs_mid': r[9]
            }	
            lstIds.append(str(r[0]))	
            lstMessage.append(dict)

        if nTotal == 0:
            return {
                "page": nPage,
                "size": nSize,
                "total": nTotal,
                "list": lstMessage,
                "lstMissile":[]
            }

        if len(lstIds) == 0:
            return {
            "page": nPage,
            "size": nSize,
            "total": nTotal,
            "list": lstMessage,
            "lstMissile":[]
        }
        
        #查询弹型
        strIds = ','.join(lstIds)
        '''获取ai_damage_strength列表'''
        strSqlSelMissile = f'''
        SELECT
            t_id,
            m_id 
        FROM
            ai_damage_strength 
        WHERE
            t_id IN ({strIds}) 
        ORDER BY
            t_id'''
        
        lstM = ConnOper.ExeGetList(strSqlSelMissile)
        lstMissile = []
        for r in lstM:
            dict = {
                't_id': r[0],
                'm_id': r[1]
            }
            lstMissile.append(dict)

        return {
            "page": nPage,
            "size": nSize,
            "total": nTotal,
            "list": lstMessage,
            "lstMissile":lstMissile
        }



    @staticmethod
    def GetAll() -> list:
        """得到全部ai目标

        Returns:
            lstMessage (list): 全部ai目标对象
        """        
        '''获取ai_target列表'''
        strSql = '''SELECT
            at_id,
            name
        FROM
            ai_target
        ORDER BY at_id DESC'''

        lst = ConnOper.ExeGetList(strSql)

        lstMessage = []
        for r in lst:
            dict = {
                'at_id': r[0],
                'name': r[1]
            }
            lstMessage.append(dict)

        return lstMessage

    @staticmethod
    def Get(nID):
        """取得某项

        Args:
            nID (int): 主键id

        Returns:
            entity (object): 取得的项
        """        
        strSql = '''SELECT
            name,
            tt_id,
            category_id,
            shape_id,
            shape_length,
            shape_width,
            shape_height,
            position_relation_id,
            bs_mid
        FROM
            ai_target 
        WHERE
            at_id=%s'''

        tupRow = ConnOper.ExeGetOneRow(strSql, (nID,))

        if tupRow is None:
            return None

        entity = CEntityai_target()
        entity.name = tupRow[0]
        entity.tt_id = tupRow[1]
        entity.category_id = tupRow[2]
        entity.shape_id = tupRow[3]
        entity.shape_length = tupRow[4]
        entity.shape_width = tupRow[5]
        entity.shape_height = tupRow[6]
        entity.position_relation_id = tupRow[7]
        entity.bs_mid = tupRow[8]
        entity.at_id = nID

        return entity
        
    def ToDictGet(self):
        dict = {
            'name':self.name,
            'tt_id':self.tt_id,
            'category_id':self.category_id,
            'shape_id':self.shape_id,
            'shape_length':self.shape_length,
            'shape_width':self.shape_width,
            'shape_height':self.shape_height,
            'position_relation_id':self.position_relation_id,
            'bs_mid':self.bs_mid
        }
        return dict

    @staticmethod
    def Exist(nID):
        """根据id判断ai目标是否存在

        Args:
            nID (int): ai目标主键

        Returns:
            res (bool): true表示存在，false表示不存在
        """        
        '''     判断某项是否存在     '''
        strSql = 'SELECT 1 FROM ai_target WHERE at_id = %s LIMIT 1'
        nCount = ConnOper.ExeGetRowCount(strSql, (nID,))
        return nCount > 0

    def Add(self) -> int:
        """添加一个ai目标

        Returns:
           res (int): 新项的id
        """        
        '''     添加项,返回添加的ID     '''
        strSql = '''
        INSERT INTO
            ai_target
        (
        	name,
        	tt_id,
        	category_id,
        	shape_id,
        	shape_length,
        	shape_width,
        	shape_height,
        	position_relation_id,
        	bs_mid
    	)
        VALUES 
        (
        %(name)s,
        %(tt_id)s,
        %(category_id)s,
        %(shape_id)s,
        %(shape_length)s,
        %(shape_width)s,
        %(shape_height)s,
        %(position_relation_id)s,
        %(bs_mid)s
        ) RETURNING at_id'''

        dicParam = {
                'name': self.name,
                'tt_id': self.tt_id,
                'category_id': self.category_id,
                'shape_id': self.shape_id,
                'shape_length': self.shape_length,
                'shape_width': self.shape_width,
                'shape_height': self.shape_height,
                'position_relation_id': self.position_relation_id,
                'bs_mid': self.bs_mid,
                }

        return ConnOper.ExeCommitAndGetValue(strSql, dicParam)

    @staticmethod
    def Delete(nID : int) -> bool:
        """删除某项

        Args:
            nID (int): 主键id

        Returns:
            res (bool): true表示删除成功，false表示删除失败
        """        
        '''    删除项，成功返回True    '''
        strSql = "DELETE FROM ai_target WHERE at_id = %s"
        nCount = ConnOper.ExeCommitAndGetAffectRow(strSql, (nID,))
        return nCount > 0

    @staticmethod
    def DeleteMulti(ids : str) -> int:
        """删除多项

        Args:
            ids (str): 逗号分隔id组成的字符串

        Returns:
            nCount (int): 受影响的行数
        """             
        '''    删除多项，成功返回True    '''
        strSql = f"DELETE FROM ai_target WHERE at_id in ({ids})"
        nCount = ConnOper.ExeCommitAndGetAffectRow(strSql)
        return nCount

    # 根据创建的实体进行更新
    def Update(self) -> bool:
        """更新某项

        Returns:
            res (bool): true表示更新成功，false表示更新失败
        """        
        strSql = '''UPDATE ai_target 
            SET 
	      name = %s,
	      tt_id = %s,
	      category_id = %s,
	      shape_id = %s,
	      shape_length = %s,
	      shape_width = %s,
	      shape_height = %s,
	      position_relation_id = %s,
	      bs_mid = %s
            WHERE
                at_id = %s'''
        
        param = (self.name,self.tt_id,self.category_id,self.shape_id,self.shape_length,self.shape_width,self.shape_height,self.position_relation_id,self.bs_mid,self.at_id)
        nCount = ConnOper.ExeCommitAndGetAffectRow(strSql, param)
        return nCount > 0

    def __str__(self) -> str:
        """toString方法

        Returns:
            str (str): 对象的对应字符串
        """        
        strInfo = f'''
            'at_id':{self.at_id}
            'name':{self.name}
            'tt_id':{self.tt_id}
            'category_id':{self.category_id}
            'shape_id':{self.shape_id}
            'shape_length':{self.shape_length}
            'shape_width':{self.shape_width}
            'shape_height':{self.shape_height}
            'position_relation_id':{self.position_relation_id}
            'bs_mid':{self.bs_mid}
       '''
        return strInfo

