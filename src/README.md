一、项目结构说明
  commons--封装公共的工具类
  config--项目配置文件
  data--依赖的数据文件、数据库工具类
  log--日志文件、日志工具类
  reports--测试报告文件
  test_case--用例配置文件、测试用例
  validate--断言工具类
  extract.yaml--接口数据中转文件
  pytest.ini--pytest框架的配置文件
  README.md--项目的说明
  run.py--用例执行主入口

二、yaml书写规范(本项目)
  1、使用“-”（横线） + 单个空格表示单个列表项
  2、使用 “:”（冒号） + 空格表示单个键值对
  3、使用"[]"或表示一组数据
  4、使用"{}"或表示一个键值表
  5、使用空格作为嵌套缩进工具。通常建议使用两个空格缩进，不建议使用 tab （甚至不支持）
    
三、配置文件书写规则
  1、用例文件字段说明
  以下所有字段支持手动写入的数据(仅可用字符串,数字需要用引号;代码里会做处理)、'$'开头的jsonpath表达式、sql语句
    id：用例id,也是索引,从0开始顺序递增即可
    feature: 用例模块
    story: 接口名称
    title: 用例标题
    requests: 请求参数集
        method: 请求方法,如get、post等;父层级-requests
        path: 接口路径(不含域名),父层级-requests
        headers: 请求头参数集,父层级-requests
            uid: 请求头参数示例,父层级-headers
        params: 请求体(表单)参数集,父层级-requests
            deviceId: 请求体参数示例,父层级-params
    validate: 断言集,父层级-requests
        assert_method: 断言方式集,父层级-validate
            path: 数据校验断言方式示例,父层级-assert_method;键名为path
            status: 数据校验断言方式示例,父层级-assert_method;键名为path,值为status(目前实现为固定用法,即断言状态码时写为status: code即可)
        compare_method: 断言方法集,父层级-validate
            path: 具体方法示例,父层级-compare_method,键名跟随assert_method填写,值目前提供三种：is、not和in,分别意为等于、不等、和包含
            status: is/not/in
        assert_field: 预期结果集,父层级-compare_method,键名跟随assert_method填写,支持手动填写或jsonpath及sql语句
            path: 操作成功
            status: '400'

  2、数据库配置文件字段说明
  目前仅可手动输入配置
    id: 配置项id,也是索引,从0开始顺序递增即可
    connect_name: 连接名称
    table_name: 表名,可以赋值Null;但sql语句需要附加库名(即库名.表名)
    host: 连接的主机地址(即ip)
    user: 连接用户名
    password: 连接密码
    charset: 编码格式(注意utf-8的编码格式需要写为utf8)
  3、日志配置文件字段说明
  目前仅可手动输入配置
      id: 配置项id
      config_name: 配置名称
      formate: 自定义的日志格式
      log_level: 日志等级(debug < info < warning < warn < error < exception < critical)
      file_level: 写入等级(同日志等级)
      out_level: 输出等级(同日志等级)
      channel: 日志打印的方式('w'为写入日志文件,'r'为输出到控制台,Null则代表既写入也输出)
      file_conf:
          path: 日志写入的目标地址的相对路径,父层级-file_conf
          size: 文件最大存放字节大小,传入字符串形式的算式(如20 * 1024 * 1024),按常用的写法做的,暂时没去支持int类型数据
          count: 最大回滚数,配置为int类型数据
          encoding: 编码格式('UTF-8')
      color: 彩色日志配置,做彩色日志看起来更清晰,所以没提供不做这个的选项;子层级配置示例如下
          DEBUG: 'green'
          INFO: 'cyan'
          WARNING: 'yellow'
          ERROR: 'bold_red'
          CRITICAL: 'bg_white'