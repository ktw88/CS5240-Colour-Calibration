# Training.py

Some initial attempt to transform the target image of a color chart to resemble the reference image of the same color chart.

Here is some important foreknowledge, that we already know there are 24 colored squares on the left side of the color chart,
and the square on the lower-right corner should be 'white'. Thus, we manually approximate the central points (y,x) of each 
square, note them down in a txt file. The programme takes an average over a small neighbouring area around the centres, e.g.,
20*20 here (which is obviously still within the colored square).

Since we know where should be 'white' on the color chart, white balancing is hence also possible here.

INPUT:
	ref_path, tar_path: The path of the reference and target raw file;
	ref_color_area_ctr.txt, tar_color_area_ctr.txt: Approximately measured centres of colored squares on the images.
OUTPUT:
	TransMatrix.txt: The linear transformation matrix (4*3);
	reference.jpg, target.jpg, result.jpg: Images in jpg format.