---


---

<h1 id="project-lakshadweep-itinerary">Project Lakshadweep Itinerary</h1>
<p>This project deals with <strong>Graph</strong> implementation of<br>
<strong>Mainland(India) &lt;–&gt; Lakshadweep</strong> Sea Transport Network and Itinerary planning from this Graph.</p>
<h1 id="ship-schedule">Ship Schedule</h1>
<p><img src="https://lh3.googleusercontent.com/2z8Vtmrg6Of5LPXO3wk0phR5nMl1Gt5PdncvPvY62u1VOy0Dp76HLTU9poiXZH91FP6-7Z9mFh0=s1440" alt="Sample Ship Schedule"></p>
<p>Manual Itinerary Planning based on above schedule is hard and will surely lead to missing a lot of possible travel options that are hard to spot in the above jumbled schedule. A small example can be found below:</p>
<p><img src="https://lh3.googleusercontent.com/Q2C6RoqyVIqVJ7RT1xCeNcH_rLpOfrBGkMkqrKD7of32HLaqmGbOXc86yWbJYhgDqofIWaJ2Obg=s1440" alt="Manual itinerary"></p>
<h2 id="steps-before-running-the-code">Steps before running the code</h2>
<ol>
<li>Extracting the above Ship Schedule manually.<br>
The <a href="http://lakport.nic.in">Ship Schedule</a> is captcha and text selection protected and hence the need to get the get the latest schedule manually as shown below.<br>
1.1 Go the <a href="http://lakport.nic.in">Home Page</a> and click <em><strong>Ship Schedule</strong></em></li>
</ol>
<h2 id="methodology">Methodology</h2>
<p><strong>NetworkX</strong> Library was used for making Graph. The library accepts any class object as node, and hence a class <em>locationNode</em> was defined with inner attributes <em>location</em> and <em>timestamp</em>. Instances of this class <em>locationNode</em> were used to represent Nodes in the graphs and the inner attributes can be accessed as <em>node.location</em> and <em>node.timestamp</em> for any <em>node</em> instance.</p>
<p>A new <em><strong>add_node(Graph, node)</strong></em> function was defined to add nodes to graph G, rather than using the Graph’s internal function <em>G.add_node</em> as the internal function considers any two exact same instances of the class <em>nodeLocation</em> as different based on their different memory location rather than comparing their internal attributes.</p>
<p>Edges between any two <em>nodes</em> have <em>ship</em> defined for it. In case of <em>travel edge</em> (Directed edge representing travelling between two nodes) <em>ship</em> is set to the <em>ship of travel</em>, and in case of <em>stay edge</em>, <em>ship</em> is set to <em>None.</em></p>
<p><em><strong>find_n_routes(Graph, source, destination, max_n_routes)</strong></em> was defined to find maximum n routes between <em>source</em> and <em>destination</em> in any  order. If <em>destination</em> is not defined, the <em>source</em> and <em>destination</em> are  considered same. The function returns a list of itineraries with each itinerary consisting a list of <em>locationNode</em> s that are then used to reconstruct the paths of each itinerary.<br>
<em><strong>print_routes()</strong></em> function defined is used to print all the routes/itineraries returned by the <em>find_n_routes()</em> function above.</p>
<h2 id="future-work">Future Work</h2>
<p>I would love to expand this project to output all the itineraries overlayed onto a map, with timestamps of each node, and also add extensive sorting options like sorting by</p>
<ul>
<li><em>Highest Contingency Itineraries</em><br>
In case a ship gets cancelled, possibility to hop onto another ship and change itinerary without much hustle would be great.</li>
<li><em>Seat Availability</em><br>
Sorting out itineraries with maximum possible seats available for <em>n</em> passengers. (Seat Availability details on <a href="http://lakport.nic.in">lakport.nic.in</a> are not available for all ships at once. We need to check for availability for each ship on each voyage separately, protected by captcha.)</li>
</ul>

