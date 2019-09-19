/**
 * Created by Administrator on 2017/8/2.
 */

// 自执行函数
(function (jq) {

    var GLOBAL_DICT = {};
    /*
    {
        'device_type_choices': (
                                    (1, '服务器'),
                                    (2, '交换机'),
                                    (3, '防火墙'),
                                )
        'device_status_choices': (
                                    (1, '上架'),
                                    (2, '在线'),
                                    (3, '离线'),
                                    (4, '下架'),
                                )
    }
     */

    // 为字符串创建format方法，用于字符串格式化
    String.prototype.format = function (args) {
        return this.replace(/\{(\w+)\}/g, function (s, i) {
            return args[i];
        });
    };

    function initial(url) {
        $.ajax({
            url: url,
            type: 'GET',  // 获取数据
            dataType: 'JSON',
            success: function (arg) {
                $.each(arg.global_dict,function(k,v){
                     GLOBAL_DICT[k] = v
                });

                /*
                 {
                 'server_list':list(server_list), # 所有数据
                 'table_config':table_config      # 所有配置
                  'global_dict':{
                        'device_type_choices': (
                                                    (1, '服务器'),
                                                    (2, '交换机'),
                                                    (3, '防火墙'),
                                                )
                        'device_status_choices': (
                                                    (1, '上架'),
                                                    (2, '在线'),
                                                    (3, '离线'),
                                                    (4, '下架'),
                                                )
                    }
                 }
                 */
                initTableHeader(arg.table_config);
                initTableBody(arg.server_list, arg.table_config);
            }
        })
    }

    function initTableHeader(tableConfig) {
        /*
         [
         {'q':'id','title':'ID'},
         {'q':'hostname','title':'主机名'},
         ]
         */
        $.each(tableConfig, function (k, v) {
            if (v.display) {
                var tag = document.createElement('th');
                tag.innerHTML = v.title;
                $('#tbHead').find('tr').append(tag);
            }
        })
    }

    function initTableBody(serverList, tableConfig) {
        /*
         serverList = [
         {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-},
         {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-},
         {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-},
         {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-},
         ]
         */
        $.each(serverList, function (k, row) {
            // row: {'id': 1, 'hostname':c2.com, create_at: xxxx-xx-xx-}
            /*
             <tr>
             <td>id</td>
             <td>hostn</td>
             <td>create</td>
             </tr>
             */
            var tr = document.createElement('tr');
            $.each(tableConfig, function (kk, rrow) {
                // kk: 1  rrow:{'q':'id','title':'ID'},         // rrow.q = "id"
                // kk: .  rrow:{'q':'hostname','title':'主机名'},// rrow.q = "hostname"
                // kk: .  rrow:{'q':'create_at','title':'创建时间'}, // rrow.q = "create_at"
                if (rrow.display) {
                    var td = document.createElement('td');
                    /*
                     if(rrow['q']){
                     td.innerHTML = row[rrow.q];
                     }else{
                     td.innerHTML = rrow.text;
                     }*/
                    // rrow['q']
                    // rrow['text']
                    // rrow.text.tpl = "asdf{n1}sdf"
                    // rrow.text.kwargs = {'n1':'@id','n2':'@@123'}
                    var newKwargs = {}; // {'n1':'1','n2':'123'}           //存放处理特殊字符，进行数据库操作后的新字典
                    $.each(rrow.text.kwargs, function (kkk, vvv) {
                        var av = vvv;
                        if(vvv.substring(0,2) == '@@'){
                            var global_dict_key = vvv.substring(2,vvv.length);
                            var nid = row[rrow.q];
                            console.log(nid,global_dict_key); // 1 "device_type_choices"
                            $.each(GLOBAL_DICT[global_dict_key],function(gk,gv){
                                if(gv[0] == nid){
                                    av = gv[1];
                                }
                            })
                        }
                        else if (vvv[0] == '@') {           //如果文本以@开头，去掉@,去除数据库中的值
                            av = row[vvv.substring(1, vvv.length)];
                        }
                        newKwargs[kkk] = av;
                    });
                    var newText = rrow.text.tpl.format(newKwargs);
                    td.innerHTML = newText;
                    $(tr).append(td);
                }
            });
            $('#tbBody').append(tr);

        })
    }

    //定义新函数xx
    jq.extend({
        xx: function (url) {
            initial(url);
        }
    })
})(jQuery);