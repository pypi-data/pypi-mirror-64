class DataTable:
    """data formats supported:
    list1:
            [
            1   ['headerA', 'headerB', 'headerC'],
            2   ['A_value', 'B_value', 'C_value'],
            3   ['A_value', 'B_value', 'C_value']
            ]
    list2:
            ︹      1        2
                    ︹       ︹
                'HeaderA' 'HeaderB'
                    ,        ,    
                'A_value' 'B_value'
                    ,        ,
                'A_value' 'B_value'
                    ︺       ︺
                    ,               ︺
    list3:
            [
                {'HeaderA':'A_value', 'HeaderB':'B_value', 'HeaderC':'C_value'},
                {'HeaderA':'A_value', 'HeaderB':'B_value', 'HeaderC':'C_value'},
                {'HeaderA':'A_value', 'HeaderB':'B_value', 'HeaderC':'C_value'}
            ]
    dict:
            ︷
                'HeaderA' 'HeaderB'
                   ‥        ‥ 
                   ︹        ︹
                'A_value' 'B_value'
                    ,        ,
                'A_value' 'B_value'
                   ︺        ︺
                    ,               ︸
    """
    def __init__(self, data, data_format):
        if data_format == 'list1':
            self.__data = {col[0]:col[1:] for col in [[line[idx] for line in data] for idx in range(len(data[0]))]}
        elif data_format == 'list2':
            self.__data = {col[0]:col[1:] for col in data}
        elif data_format == 'list3':
            self.__data = {header:[line[header] for line in data] for header in data[0].keys()}
        elif data_format == 'dict':
            self.__data = data
        else:
            raise ValueError('format only surport "list1" "list2" "list3" "dict"')
        self.__rows_count = len(list(self.__data.values())[0])
    def __getitem__(self, data_format): # 按指定格式导出数据
        if data_format == 'list1':
            return [list(self.__data.keys())] + [[col_values[idx] for col_values in self.__data.values()] for idx in range(self.__rows_count)]
        elif data_format == 'list2':
            return [[items[0]] + items[1] for items in self.__data.items()]
        elif data_format == 'list3':
            return [{item[0]:item[1][idx] for item in list(self.__data.items())} for idx in range(len(list(self.__data.values())[0]))]
        elif data_format == 'dict':
            return self.__data
        else: 
            raise ValueError('only surport format "list1" "list2" "list3" "dict"')
    def to_str_table(self, filler=' ', delimiter='|', width_addition=4, indent=0, alignment='^'): # 导出为字符串表格
        widths = []
        for (header, col_values) in self.__data.items():
            max_width = max([len(value.encode('gbk')) for value in [header] + col_values])
            widths.append(max_width + width_addition)
        return '\n'.join([delimiter + delimiter.join([f"{cell_value:{filler}{alignment}{widths[col_idx] - (len(cell_value.encode('gbk')) - len(cell_value))}}" for (col_idx, cell_value) in enumerate(row_values)]) + delimiter for row_values in self.__getitem__('list1')])