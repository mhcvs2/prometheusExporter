Scalable Prometheus Exporter 
==============================

operate
-----------
* create a python package with name "name_exporter", like "mysql_exporter"
* write defination in metrics.py, metrics name  must start with "name_" like "mysql_"
* handler function in handler.py, function name must start with metrics name, end with "_handler"
* update exporter.cnf
   <pre><code>
   [name]
   par1=value1
   par2=value2
   </code></pre>
<p>
Run "python exporter.py ./exporter.cnf"<br>
Then this exporter will run, and function in handler.py can get a dict parameter like {par1:value1,par2:value2}
</p>
    