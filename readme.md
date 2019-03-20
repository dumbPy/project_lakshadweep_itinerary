---


---

<h1 id="project-lakshadweep-itinerary">Project Lakshadweep Itinerary</h1>
<h2 id="introduction">Introduction</h2>
<p><a href="https://en.wikipedia.org/wiki/Lakshadweep">Lakshadweep</a> is a group of islands off south western coast of India, and has a lots of scenic and <a href="https://www.google.co.in/search?q=lakshadweep&amp;source=lnms&amp;tbm=isch">Beautiful Untouched Beaches</a> and <a href="https://www.google.co.in/search?q=lakshadweep+Lagoons&amp;source=lnms&amp;tbm=isch">Lagoons</a> worth exploring. The Islands are open to Tourists under permit from the Administrative Officer (<a href="mailto:lk-secadm@nic.in">email</a>). The mode of transport however, is limited to Govt. operated Ships that mainly ply between Mainland India (Kochi and Mangalore port) and the islands of Lakshadweep. The prime purpose of these Ships is to satisfy the needs of the Islanders that depend solely on supplies from Mainland India. Hence, the Ship Schedule is mostly dependent on the Cargo needs of each Island and is prepared fresh every month and frequency is very low. The seat availability is very limited and gets filled within a couple of days of Ship Schedule announcement for any given month.<br>
There is a Daily Flight from <a href="https://www.google.co.in/search?q=kochi+to+agatti">Kochi to Agatti</a> operated by Air India, but the inter-Island transport is again limited to the same above Ships. The same ships are also used by the Islanders for transport, causing a stable internal demand for these limited seats.<br>
Hence the need to come up with a suitable Itinerary planning method was felt by the author, and gave rise to this project.</p>
<p>This project deals with <strong>Directed Graph</strong> implementation of<br>
<strong>Mainland(India) &lt;–&gt; Lakshadweep</strong> Sea Transport Network and Itinerary planning from this Graph.</p>
<h2 id="ship-schedule">Ship Schedule</h2>
<p>Each Month, the Lakshadweep Administration publishes a new Schedule for these ships. An example of this schedule can be found below:<br>
<img src="Images/original_schedule.png" alt="Sample Ship Schedule"></p>
<p>Manual Itinerary Planning based on above schedule is hard and will surely lead to missing a lot of possible travel options that are hard to spot in the above jumbled schedule. A small example can be found below:</p>
<p><img src="Images/Manual Itinerary Sample.jpg" alt="Manual itinerary"></p>
<h2 id="steps-before-running-the-code">Steps before running the code</h2>
<h3 id="extracting-the-above-ship-schedule-manually.">Extracting the above Ship Schedule manually.</h3>
<p>The <a href="http://lakport.nic.in">Ship Schedule</a> is captcha and text selection protected Run the <a href=get_new_schedule.py>get_new_schedule.py</a> to download latest Schedule</p>
<p>The Code will extract the required Schedule Table from the HTML file generated</p>
<h2 id="methodology">Methodology</h2>
<h3 id="laymans">Layman’s:</h3>
<p><img src="Images/sample_itinerary.png" alt="enter image description here"><br>
Above Network shows Travel and Stay as Edges with related Data. Note: <em>‘ship’:None</em> represents Stay at the island representing same Island by two different nodes at two different timing.</p>
<h3 id="technical">Technical</h3>
<p>(You may neglect this part)<br>
<a href="Notebooks/how_it_works.ipynb"><strong>how_it_works.ipynb</strong></a> to understand the working of the project.</p>
<h2 id="future-work">Future Work</h2>
<li><em><strong>[Done]</strong> I would love to expand this project to output all the itineraries overlayed onto a map, with timestamps of each node.</em><br>

<li><em> Add extensive sorting options like sorting by</em><br>
<ul>
<li><em>Highest Contingency Itineraries</em><br>
In case a ship gets cancelled, possibility to hop onto another ship and change itinerary without much hustle would be great.</li>
<li><em>Seat Availability</em><br>
Scraping Seat Availability from <a href="http://lakport.nic.in">lakport.nic.in</a>.<br>
Sorting out itineraries with maximum possible seats available for <em>n</em> passengers. (Seat Availability details on <a href="http://lakport.nic.in">lakport.nic.in</a> are not available for all ships at once. We need to check for availability for each ship on each voyage separately, protected by captcha.)</li>
</ul>

