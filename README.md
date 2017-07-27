Scalable Prometheus Exporter 
==============================

operate
-----------
* create a python package with name "name_exporter"
* write defination in metrics.py and handler function in handler.py
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
    