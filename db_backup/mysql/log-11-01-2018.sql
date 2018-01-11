-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: log
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(100) NOT NULL,
  `body` mediumtext NOT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `author` (`author`,`body`),
  FULLTEXT KEY `author_2` (`author`,`body`),
  FULLTEXT KEY `author_3` (`author`,`body`),
  FULLTEXT KEY `author_4` (`author`,`body`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
INSERT INTO `logs` VALUES (1,'yebin','<p>普通用户新建日志测试一。</p>\r\n\r\n<p>编辑测试。</p>\r\n','2017-11-11 16:38:15'),(2,'yebin','<p>普通用户新建日志测试二。</p>\r\n','2017-11-11 16:38:40'),(3,'yebin','<p>普通用户新建日志测试三。</p>\r\n','2017-11-11 16:38:52'),(4,'admin','<p>新建管理员日志测试一。</p>\r\n\r\n<p>编辑测试。</p>\r\n','2017-11-11 17:39:45'),(5,'admin','<p>新建管理员日志测试二。</p>\r\n','2017-11-11 17:40:00'),(6,'admin','<p>新建管理员日志测试三。</p>\r\n','2017-11-11 17:40:12'),(14,'yebin','<p>用手机发布日志测试。</p>\r\n','2017-11-11 19:31:07'),(16,'yebin','<p>数据库表数据提取翻页显示测试。</p>\r\n','2017-11-13 03:06:40'),(17,'admin','<p>管理员日志删除和日志翻页测试。</p>\r\n','2017-11-13 03:07:25'),(18,'admin','<p>翻页测试二。</p>\r\n','2017-11-13 03:07:43'),(19,'yebin','<p>翻页测试二。</p>\r\n','2017-11-13 03:08:03'),(20,'admin','<p>导航增加新建按钮。</p>\r\n','2017-11-13 06:57:54'),(21,'yebin','<p>工作日志项目增加翻页功能，增加删除用户和删除日志的确认功能。</p>\r\n','2017-11-13 10:42:35'),(22,'yebin','<p>1. 上海新收犯监狱维护。</p>\r\n\r\n<p>2. 安装windows7到办公机，配置为双启动，并将linux分区下的工作文件转移至windows分区。</p>\r\n','2017-11-14 10:30:25'),(23,'yebin','<p>1、放弃nginx反向代理https服务，弃用uWSGI；</p>\r\n\r\n<p>2、直接采用systemd的service托管flask网站；</p>\r\n\r\n<p>3、在flask内部启用ssl（mainpage项目）；</p>\r\n\r\n<p>4、增加小站监控登录列，在用户名称上悬浮显示管理IP。</p>\r\n','2017-11-15 15:34:50'),(24,'yebin','<p>为日志项目和小站项目增加翻页功能，小站在线监控翻页功能暂未完成。</p>\r\n','2017-11-16 10:03:02'),(25,'yebin','<p>1、完成小站在线状态页面的翻页的功能；</p>\r\n\r\n<p>2、增加域名解析：doc.satelc.com，端口为 8021；</p>\r\n\r\n<p>3、将卫星远端站综合管理首页由域名 myblog.satelc.com 改为 satelc.com；</p>\r\n\r\n<p>4、在小站在线状态页面增加总小站数、总在线数、当前页面小站数和当前页面在线数。</p>\r\n','2017-11-17 08:44:51'),(26,'yebin','<p>关于数据库搜索的几个参考链接：</p>\r\n\r\n<ul>\r\n	<li><a href=\"https://www.v2ex.com/t/274600\" target=\"_blank\">请问 Flask-WhooshAlchemy 支持中文检索是有问题吗？</a></li>\r\n	<li><a href=\"https://github.com/Revolution1/Flask-WhooshAlchemyPlus\" target=\"_blank\">Flask-WhooshAlchemyPlus</a></li>\r\n	<li><a href=\"https://github.com/bkabrda/flask-whooshee\" target=\"_blank\">Flask-Whooshee</a></li>\r\n	<li><a href=\"https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-full-text-search\" target=\"_blank\">The Flask Mega-Tutorial, Part X: Full Text Search</a></li>\r\n	<li><a href=\"https://stackoverflow.com/questions/28786515/two-ways-of-creating-a-flask-sqlalchemy-basequery-object-only-one-works-why\" target=\"_blank\">Two ways of creating a flask-SQLAlchemy BaseQuery object - only one works, why?</a></li>\r\n</ul>\r\n','2017-11-20 15:34:40'),(27,'yebin','<p>分别为普通用户和管理员增加数据库模糊查询以及查询结果分页显示功能，每次查询将查询关键字保存到全局变量以实现分页。</p>\r\n','2017-11-21 09:59:58'),(28,'yebin','<p>1、增加myblog的查询功能；</p>\r\n\r\n<p>2、用js实现下拉菜单，实现在特定范围内查询，包括小站和公告；</p>\r\n\r\n<p>3、将查询结果的html页面的jinja2跳转由flask的路由改为url_for，排除单击下一页后点击条目无法进入对应页面的bug；</p>\r\n\r\n<p>4、将每种查询范围对应的路由函数的名称通过变量传递给jinja2前端，实现翻页功能动态获取当前查询函数路由的功能。</p>\r\n','2017-11-22 06:36:46'),(29,'yebin','<p>2017-11-23（补）</p>\r\n\r\n<p>1. 将树莓派的温度每隔一分钟写入到数据库；</p>\r\n\r\n<p>2. 修改论文，将所有&ldquo;段后6&rdquo;改为&ldquo;段后0&rdquo;。</p>\r\n','2017-11-23 23:56:03'),(30,'yebin','<p>1. 金山民防办维护，天线极化电机故障，垂直极化信标改为953兆赫；</p>\r\n\r\n<p>2. 初步实现小站监控温度实时显示，需改善的是增加温度所属单位。</p>\r\n','2017-11-24 10:50:48'),(31,'yebin','<p>修复小站在线状态中温度显示的bug，现在该功能可以实时显示每个用户终端的温度。</p>\r\n','2017-11-24 17:33:21'),(32,'yebin','<p>1. 增加微信公众号关键字自动回复功能，发送用户终端名，回复终端在线状态和设备温度；</p>\r\n\r\n<p>2. 完成小站在线状态和温度的实时监控；</p>\r\n\r\n<p>3. 终端（Pi3）脚本待备份；</p>\r\n\r\n<p>4. 备份源代码（待办）。</p>\r\n','2017-11-26 14:01:51'),(33,'yebin','<p>湖北无委项目：</p>\r\n\r\n<p>1. 培训及考试方案；</p>\r\n\r\n<p>2. 无人机安装及4G安装；</p>\r\n\r\n<p>3. 黄石地面站功放安装及卫星通信调试。</p>\r\n\r\n<p>崇明民防：</p>\r\n\r\n<p>1. 发电机保养；</p>\r\n\r\n<p>2. 例行维护。</p>\r\n\r\n<p>虹口民防：发电机保养，用户有费用疑问，需要向项目经理确认。</p>\r\n\r\n<p>硕士论文：</p>\r\n\r\n<p>1. 增加实时温度显示；</p>\r\n\r\n<p>2. 增加微信公众平台接入；</p>\r\n\r\n<p>3. 增加查询；</p>\r\n\r\n<p>4. 控制器增加数据库和 web request post 脚本；</p>\r\n\r\n<p>5. 修正参考文件引用序号；</p>\r\n\r\n<p>6. 增加三个系统设计结构图；</p>\r\n\r\n<p>7. 增加第四章树莓派等外设图的文字描述；</p>\r\n\r\n<p>8. 图形裁边；</p>\r\n\r\n<p>9. 断后格式改为 0 磅。</p>\r\n\r\n<p>论文待办：</p>\r\n\r\n<p>1. 修改英文摘要；</p>\r\n\r\n<p>2. 查重。</p>\r\n','2017-11-28 09:33:35'),(34,'yebin','<p>1. 诺特和上海监狱的合同已签，需要发OA采购申请，向蓝波采购发射机；</p>\r\n\r\n<p>2. 湖北无委无人机视频转换设备须加上服务费，约1300元，由我方负责采购；</p>\r\n\r\n<p>3. 学费已交；</p>\r\n\r\n<p>4. 考虑更换上海移动4G套餐；</p>\r\n\r\n<p>5. 为mainpage项目增加翻页功能，优化不同用户显示不同文档功能代码，查询功能待增加。</p>\r\n','2017-11-29 07:36:44'),(35,'yebin','<p>1. 湖北无委项目：</p>\r\n\r\n<p>已联系冠艺（HDMI无线传输）张经理，确定采购清单，由我方进行采购和安装。</p>\r\n\r\n<p>2. 民防：</p>\r\n\r\n<p>长宁和崇明民防下周四之前维护，周四演练，长宁10至12月的维护单；</p>\r\n\r\n<p>虹口民防发电机保养待办。</p>\r\n\r\n<p>3. mainpage 项目：</p>\r\n\r\n<p>增加用户文档显示页面的翻页功能；</p>\r\n\r\n<p>增加按文档标题和按文档内容搜索功能。</p>\r\n\r\n<p>4. 增加cgi模块，对搜索关键字进行转义，防止sql注入式攻击。</p>\r\n','2017-11-30 06:58:54'),(36,'yebin','<p>需变更还原项：</p>\r\n\r\n<p>测试条目中，台式机变更为了上海消防地面站。</p>\r\n','2017-11-30 08:35:20'),(37,'yebin','<p>昨晚对小站监控的温度显示进行了修复，排除基本故障。但是由于浏览器每次访问时才对监控页面发出请求，所以会出现页面刚出现时某些站的温度没有显示，可以对显示数据的获取作进一步优化，如不采用小站推送温度数据直接显示，而采用通过数据库读取数据显示，或者在温度推送前对温度值进行初始化操作。</p>\r\n','2017-11-30 23:05:18'),(38,'yebin','<p>2017年12月6日：</p>\r\n\r\n<p>1、长宁民防维护，调整天控器信标参数；</p>\r\n\r\n<p>2、静安民防维护，调整KVM。</p>\r\n','2017-12-19 09:28:12'),(39,'yebin','<p>2017年12月8日：</p>\r\n\r\n<p>湖北无委项目通信指挥车状态检查，原车电瓶无法启动车辆，用充电器给原车电瓶充电后恢复。</p>\r\n\r\n<p>注意：引擎盖内的电瓶不是发动机启动电瓶，是原车辅助电瓶。发电机启动电瓶在驾驶位下方的铁板内。</p>\r\n\r\n<p>启动车载发电机，给发电机电瓶和UPS电瓶充电。</p>\r\n','2017-12-19 09:31:13'),(40,'yebin','<p>2017年12月9日：</p>\r\n\r\n<p>1、去黄石无委取修好的卫星功放；</p>\r\n\r\n<p>2、去黄石地面站安装功放，并测试，结果运行正常；</p>\r\n\r\n<p>3、部署远程监控终端，修改570L的串口远程通信参数。</p>\r\n','2017-12-19 09:34:03'),(41,'yebin','<p>2017年12月10日：</p>\r\n\r\n<p>1、准备湖北无委培训文档；</p>\r\n\r\n<p>2、准备湖北无委操作文档。</p>\r\n','2017-12-19 09:35:04'),(42,'yebin','<p>2017年12月11日：</p>\r\n\r\n<p>1、上午部署湖北无委会议中心；</p>\r\n\r\n<p>2、下午勘察演练现场。</p>\r\n','2017-12-19 09:37:22'),(43,'yebin','<p>2017年12月12日：</p>\r\n\r\n<p>演练现场操作培训，安排演练流程，测试所有设备，排除所有故障。</p>\r\n\r\n<p>关于4G机动宽带：</p>\r\n\r\n<p>http://192.168.90.129:2323/dss_90/client/#</p>\r\n\r\n<p>http://192.168.90.129:2323/ietc_80/client/#</p>\r\n\r\n<p>admin<br />\r\nNULL</p>\r\n\r\n<p>show hssauthdata<br />\r\nshow hsduserdata<br />\r\nshow dssuserdata</p>\r\n\r\n<p>sync</p>\r\n\r\n<p>http://192.168.90.55/dispatcher/controller</p>\r\n\r\n<p>admin<br />\r\n111111</p>\r\n\r\n<p>工控机显卡故障</p>\r\n','2017-12-19 09:38:19'),(44,'yebin','<p>2017年12月13日：</p>\r\n\r\n<p>湖北无委荷田酒店会议厅理论培训。</p>\r\n','2017-12-19 09:38:40'),(45,'yebin','<p>2017年12月14日：</p>\r\n\r\n<p>正式演练。</p>\r\n\r\n<p>中心频率：1141</p>\r\n\r\n<p>带宽：4M</p>\r\n\r\n<p>车：<br />\r\ntx: 1140<br />\r\nrx: 1142</p>\r\n\r\n<p>地面站：<br />\r\ntx: 1142<br />\r\nrx: 1140</p>\r\n','2017-12-19 09:40:46'),(46,'yebin','<p>2017年12月15日：</p>\r\n\r\n<p>湖北无委演练后的收尾工作，包括再次培训和文档整理等。</p>\r\n\r\n<p>另：</p>\r\n\r\n<p>增加一台服务器：111.47.20.166（中国移动）</p>\r\n\r\n<p>域名：hxwulian.cn</p>\r\n\r\n<p>用户名：yebin</p>\r\n\r\n<p>密码：同原服务器配置。</p>\r\n','2017-12-19 09:43:53'),(47,'yebin','<p>2017年12月25日</p>\r\n\r\n<p>崇明民防维护：</p>\r\n\r\n<p>1、支撑脚控制器偶尔不灵；</p>\r\n\r\n<p>2、发电机电瓶需要外接电瓶才能启动；</p>\r\n\r\n<p>3、下次每两个月做一次维护，带维护报告；</p>\r\n\r\n<p>4、发电机待保养。</p>\r\n','2017-12-26 13:29:37'),(48,'yebin','<p>服务器：</p>\r\n\r\n<p>品牌：Lenovo 联想</p>\r\n\r\n<p>型号：万全 R680 G7</p>\r\n\r\n<p>配置：SAS RAID</p>\r\n\r\n<p>电源：AC200-240V 50Hz 14A</p>\r\n\r\n<p>生产日期：2011年08月12日</p>\r\n\r\n<p>SO 号：0005989424</p>\r\n\r\n<p>服务网址：http://support.lenovo.com.cn</p>\r\n\r\n<p>出厂编号：NC00731230</p>\r\n\r\n<p>联想（北京）有限公司</p>\r\n','2017-12-27 09:05:34'),(49,'yebin','<p>维修新收监iPad2：</p>\r\n\r\n<p>1、更换外屏；</p>\r\n\r\n<p>2、重置系统；</p>\r\n\r\n<p>3、检测电池；</p>\r\n\r\n<p>4、删除用户（钱树博）。</p>\r\n','2017-12-29 08:55:09'),(50,'yebin','<p>About IoT:</p>\r\n\r\n<p>https://thinger.io/</p>\r\n\r\n<p>https://www.pega.com/</p>\r\n\r\n<p>https://open.iot.10086.cn/</p>\r\n\r\n<p>http://cloud.usr.cn/</p>\r\n\r\n<p>http://iot.open.qq.com/</p>\r\n\r\n<p>http://qinfei.glrsmart.com/2017/07/18/linuxchun-jiao-ben-shi-xian-mqttyu-chuan-kou-tou-chuan/</p>\r\n\r\n<p>树莓派USB转串口：</p>\r\n\r\n<p>http://www.voidcn.com/article/p-ghniinor-ss.html</p>\r\n\r\n<p>物联网：</p>\r\n\r\n<p>IoT(TICK):&nbsp;Telegraf, InfluxDB,&nbsp;Chronograf,&nbsp;Kapacitor</p>\r\n\r\n<p>IoT Stack:</p>\r\n\r\n<p>Mosca - MQTT Broker</p>\r\n\r\n<p>Telegraf - Ingestion Engine</p>\r\n\r\n<p>InfluxDB - Time-Seriers Database</p>\r\n\r\n<p>Chronograf - Dashboard</p>\r\n\r\n<p>Node-Red - Rules Engine</p>\r\n\r\n<p>Popular: LoRa / NB-IoT</p>\r\n','2018-01-03 05:27:44'),(51,'yebin','<p>The Flask Mega-Tutorial, Part XI: Email Support:</p>\r\n\r\n<p>https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support-legacy</p>\r\n\r\n<p>Open Source Time Series Platform:</p>\r\n\r\n<p>https://www.influxdata.com/time-series-platform/</p>\r\n\r\n<p>IoT influxdata documents:</p>\r\n\r\n<p><a href=\"https://docs.influxdata.com/\" target=\"_blank\">https://docs.influxdata.com/</a></p>\r\n\r\n<p>-------------------------------------</p>\r\n\r\n<p>Workspace Name &amp; URL：<br />\r\nYour workspace name is fly and your URL is https://flycrew.slack.com.<br />\r\nWebhook URL：<br />\r\nhttps://hooks.slack.com/services/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<br />\r\nSending Messages：<br />\r\nYou have two options for sending data to the Webhook URL above:<br />\r\nSend a JSON string as the payload parameter in a POST request<br />\r\nSend a JSON string as the body of a POST request<br />\r\nFor a simple message, your JSON payload could contain a text property at minimum. This is the text that will be posted to the channel.<br />\r\nA simple example:<br />\r\npayload={&quot;text&quot;: &quot;This is a line of text in a channel.\\nAnd this is another line of text.&quot;}</p>\r\n','2018-01-04 01:38:25'),(52,'yebin','<p>How&nbsp;To&nbsp;Monitor&nbsp;System&nbsp;Metrics&nbsp;with&nbsp;the&nbsp;TICK&nbsp;Stack&nbsp;on&nbsp;Ubuntu&nbsp;16.04&nbsp;|&nbsp;DigitalOcean:</p>\r\n\r\n<p>https://www.digitalocean.com/community/tutorials/how-to-monitor-system-metrics-with-the-tick-stack-on-ubuntu-16-04</p>\r\n\r\n<p>How&nbsp;to&nbsp;install&nbsp;and&nbsp;configure&nbsp;Node-RED&nbsp;on&nbsp;Ubuntu&nbsp;16.04&nbsp;|&nbsp;DigitalOcean:</p>\r\n\r\n<p>https://www.digitalocean.com/community/tutorials/how-to-connect-your-internet-of-things-with-node-red-on-ubuntu-16-04</p>\r\n\r\n<p>MQTT Publish-Python MQTT Client Examples:</p>\r\n\r\n<p>http://www.steves-internet-guide.com/publishing-messages-mqtt-client/</p>\r\n\r\n<p>----------------------------------</p>\r\n\r\n<p>Some ports:</p>\r\n\r\n<p>influx:</p>\r\n\r\n<p>http://111.47.20.166:8888</p>\r\n\r\n<p>telegraf: 8086</p>\r\n\r\n<p>InfluxDB HTTP service: 8086</p>\r\n\r\n<p>&nbsp;RPC service for backup and restore: 8088</p>\r\n\r\n<p>kapacitor: 9092</p>\r\n\r\n<p>mosquitto: 1883</p>\r\n\r\n<p>node-red: 1880</p>\r\n\r\n<p>Thinger.io: 8022</p>\r\n\r\n<p>mongodb: 27017 (sudo lsof -i -ac mongod)</p>\r\n','2018-01-04 04:41:17'),(53,'yebin','<p>https://thingsboard.io/docs/reference/mqtt-api/</p>\r\n\r\n<p>http://docs.thinger.io/linux/</p>\r\n\r\n<p><a href=\"https://open.iot.10086.cn/\" target=\"_blank\">https://open.iot.10086.cn/</a></p>\r\n\r\n<p>基于Kubernetes和OpenStack的开源项目在物联网的应用：</p>\r\n\r\n<p>https://my.oschina.net/caicloud/blog/682968</p>\r\n\r\n<p>用于IoT应用程序开发的10大开源软件:</p>\r\n\r\n<p>http://iot.it168.com/a2017/0315/3104/000003104932.shtml</p>\r\n\r\n<p>https://devicehub.net/</p>\r\n\r\n<p>http://documentation.sitewhere.io/overview.html</p>\r\n\r\n<p>https://docs.particle.io/guide/getting-started/intro/raspberry-pi/</p>\r\n\r\n<p>https://thingspeak.com/</p>\r\n\r\n<p>http://www.openremote.com/community/</p>\r\n\r\n<p>https://www.kaaproject.org/getting-started/</p>\r\n\r\n<p>https://devicehive.com/</p>\r\n','2018-01-08 02:19:47'),(54,'yebin','<p>钉钉机器人（卫星终端控制器报警机器人）webhook：</p>\r\n\r\n<p>https://oapi.dingtalk.com/robot/send?access_token=14954f5339c168f1f0089b295104dd36bb38796bcedb2b46761d74230cef5228</p>\r\n\r\n<p>Python socket network programming:</p>\r\n\r\n<p>https://pythontips.com/2013/08/06/python-socket-network-programming/</p>\r\n\r\n<p>PYHEARTBEAT - DETECTING INACTIVE COMPUTERS (PYTHON RECIPE):</p>\r\n\r\n<p>https://code.activestate.com/recipes/52302-pyheartbeat-detecting-inactive-computers/</p>\r\n','2018-01-09 01:20:42'),(55,'yebin','<p>海康威视：</p>\r\n\r\n<p>在线帮助中心：www.hikvision.com/cn/support_list_55.html</p>\r\n\r\n<p>电话：0571-88075998 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>\r\n\r\n<p>技术服务微信：海康威视客户服务</p>\r\n\r\n<p>邮箱：market@hikvision.com &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>\r\n\r\n<p>技术服务电话：400-700-5998</p>\r\n\r\n<p>传真：0571-88805843 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>\r\n\r\n<p>技术服务邮箱：400@hikvision.com</p>\r\n\r\n<p>邮编：310051 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>\r\n\r\n<p>官方通讯地址：杭州市滨江区阡陌路555号</p>\r\n','2018-01-10 03:24:06'),(56,'yebin','<p>关于 thinger.io 自建平台：</p>\r\n\r\n<p>http://111.47.20.166:8022/#/settings</p>\r\n\r\n<p>每次从一个新的地方访问时，要配置一下。在第一个输入框的IP地址后面加上端口号&ldquo;:8022&rdquo;，然后点击&ldquo;Update&rdquo;，再点击&ldquo;Back to the Application&rdquo;，然后用创建的账号就可以登录。</p>\r\n\r\n<p>原因是这个平台默认是80端口，因为没有备案，在后台配置文件中改成了8022端口，所以每次从一个新的电脑登录，都要配置一下登录的端口号。</p>\r\n\r\n<p>关于 thinger.io 项目：</p>\r\n\r\n<p>https://hackaday.io/project/6329-open-source-iot-platform-thingerio/details</p>\r\n\r\n<p>https://github.com/thinger-io</p>\r\n','2018-01-10 13:23:34'),(57,'yebin','<p>湖北省武汉市武昌区尚隆路60号</p>\r\n\r\n<p>430060</p>\r\n\r\n<p>宋智勇</p>\r\n\r\n<p>18008629130</p>\r\n\r\n<p>湖北省无线电管理委员会办公室</p>\r\n','2018-01-11 03:20:50');
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `todo`
--

DROP TABLE IF EXISTS `todo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `todo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(255) NOT NULL,
  `complete` tinyint(1) NOT NULL DEFAULT '0',
  `user` varchar(50) NOT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `todo`
--

LOCK TABLES `todo` WRITE;
/*!40000 ALTER TABLE `todo` DISABLE KEYS */;
INSERT INTO `todo` VALUES (1,'待办测试项一',1,'yebin','2018-01-03 06:39:28'),(2,'待办测试项二',1,'yebin','2018-01-03 06:39:37'),(3,'待办测试项三',1,'yebin','2018-01-03 06:39:47'),(4,'待办测试项4',1,'yebin','2018-01-03 06:39:57'),(5,'待办测试项5',1,'yebin','2018-01-03 06:40:04'),(6,'待办测试项6',1,'yebin','2018-01-03 06:40:11'),(7,'To do list 7',1,'yebin','2018-01-03 06:40:20'),(8,'To do list 8',1,'yebin','2018-01-03 06:40:28'),(9,'To do list 9',1,'yebin','2018-01-03 06:40:35'),(10,'To do list 10',1,'yebin','2018-01-03 06:40:42'),(11,'TESTING TODO LIST.',1,'yebin','2018-01-03 07:14:12'),(12,'测试待办事项功能。',1,'yebin','2018-01-03 07:14:28'),(13,'换灯泡。',0,'yebin','2018-01-03 07:36:28'),(14,'2018年1月移动套餐结束时换成188无限流量套餐。',0,'yebin','2018-01-03 07:37:16'),(15,'湖北无委项目4G安装调试。',0,'yebin','2018-01-03 07:37:33'),(16,'开4G发票。',0,'yebin','2018-01-03 07:37:46'),(17,'黄石地面站控制器加入网络判断脚本。',1,'yebin','2018-01-03 07:38:12'),(18,'维修新收监iPad2中控。',1,'yebin','2018-01-03 07:38:33'),(19,'新收监图传更换及安装吸盘。',0,'yebin','2018-01-03 07:39:01'),(20,'金山民防车顶摄像机换回用户购买的型号。',0,'yebin','2018-01-03 07:39:27'),(21,'更换虹口民防指挥车左侧扬声器。',0,'yebin','2018-01-03 07:39:49'),(22,'虹口民防发电机保养。',0,'yebin','2018-01-03 07:40:02'),(23,'崇明民防发电机保养。',0,'yebin','2018-01-03 07:40:17'),(24,'崇明民防支撑腿故障。',0,'yebin','2018-01-03 07:40:33'),(25,'虹口民防4G待定。',0,'yebin','2018-01-03 07:40:46'),(26,'静安民防更换设备清单：工控机、KVM 和倒车影像。',0,'yebin','2018-01-03 07:41:15'),(27,'长宁民防警报器故障。',0,'yebin','2018-01-03 07:41:34'),(28,'湖北无委指挥车工控机和车顶右摄像头故障。',0,'yebin','2018-01-03 07:42:20'),(29,'Send email hourly to display the status of remote terminals.',1,'yebin','2018-01-04 01:05:22'),(30,'小站监控增加定时发送按钮和主动发送按钮。',0,'yebin','2018-01-04 10:00:52'),(31,'微信发消息添加日志和待办。',0,'yebin','2018-01-04 10:02:47'),(32,'向远端站中增加数据库清理脚本',0,'yebin','2018-01-05 00:45:14'),(33,'为”http://111.47.20.166:8888/“增加登录认证功能（Flask）',0,'yebin','2018-01-05 01:18:29'),(34,'influx may need openvpn',0,'yebin','2018-01-05 01:46:35'),(35,'将todo改为socketio',0,'yebin','2018-01-06 00:27:08'),(36,'mqtt 和influx通过设备id添加识别设备',0,'yebin','2018-01-06 00:28:01'),(37,'去掉telegraf系统的用户授权，通过flask实现。',1,'yebin','2018-01-06 01:58:15'),(38,'http://docs.thinger.io/',0,'yebin','2018-01-06 02:46:20'),(39,'钉钉webhook',1,'yebin','2018-01-06 03:21:20'),(40,'用测试手机号发起钉钉群聊，然后退群，用钉钉机器人的webhook发送报警信息。',1,'yebin','2018-01-06 09:45:19'),(41,'钉钉机器人 https://www.jianshu.com/p/418e4ffbb4e3',1,'yebin','2018-01-06 09:45:56'),(42,'服务器部署：http://docs.thinger.io/deployment/',1,'yebin','2018-01-06 10:01:49'),(43,'zabbix opensource ?',0,'yebin','2018-01-07 15:45:31'),(44,'heartbeat socket to confirm client\'s online',0,'yebin','2018-01-09 12:32:23'),(45,'backup server database',0,'yebin','2018-01-10 02:49:15'),(46,'backup client\'s scripts',0,'yebin','2018-01-10 02:49:30'),(47,'增加一个发送邮件的脚本，用于客户端以及服务器的终端下发送邮件。',0,'yebin','2018-01-10 07:29:01'),(48,'联系海康，邮件内容不对。',0,'yebin','2018-01-10 13:24:15'),(49,'停掉chat服务，将某些服务做合并，以减小系统内存开销。',0,'yebin','2018-01-10 13:25:41'),(50,'将消息合并导出为一个文本文件，发送文本文件附件到邮箱和机器人。',0,'yebin','2018-01-10 23:10:24');
/*!40000 ALTER TABLE `todo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'叶彬','yebin@satelc.com','admin','$5$rounds=535000$be.HH4OImr56mMfF$qz8QPlNa8ZT/QCXKhhKZoVZ5zlT3ZjAJ65E0AeIAXHD','2017-11-11 16:33:07'),(2,'叶彬','yebin@satelc.com','yebin','$5$rounds=535000$RiEzlUYbqPOYcCNd$n9ZjuA0skG.nmDSjoxWeMsaV568uQmZiFVgbhsINvk9','2017-11-11 16:33:34'),(3,'赵冬梅','zhaodongmei@satelc.com','zhaodongmei','$5$rounds=535000$HY8OxXwGfDqI.gXK$PyGM7JnXZ0bsjJwF3aYeUpYOiZ.ltyyEzXchbqMBsd.','2017-11-16 06:07:12'),(4,'高建','gaojian@satelc.com','gaojian','$5$rounds=535000$ZGMPWF0veXNR3GIb$uWGvlEoFR/jH7QI.N2CN7yOz1vK1XdXobiY9cSRF5tA','2017-11-16 06:08:11'),(5,'高玉广','gaoyuguang@satelc.com','gaoyuguang','$5$rounds=535000$B986XCwA/XdQlSik$Wgl8R486bOSde1VlHADh4ZKmF3vseh9LmnR2eCMbVdC','2017-11-16 06:09:26');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-01-11 14:45:14
