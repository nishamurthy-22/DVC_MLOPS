import gdown
output = "datasets/dataset2.zip"
url = "https://drive.google.com/file/d/1YH1U_d8G7BixL68njr0W8BuL85Tv31bf/view?usp=share_link"
gdown.download(url=url, output=output, quiet=False, fuzzy=True)