import pandas as pd 
import scimate.mappingtools as mapt
import matplotlib.pyplot as plt

test_folder = "tests/"
test_file = "out4.txt"


if __name__== "__main__":
	df = pd.read_table(test_folder + test_file, comment = "#")
	df_out,i = mapt.test_dataset(df,.04,mapt.pol2)
	print(i)
	# fig,ax = plt.subplots()
	# mapt.sliderplot(df_out,ax)
	# plt.show()


