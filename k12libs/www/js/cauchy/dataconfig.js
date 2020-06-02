let predatasets = [];
let debug = true;
let datasets_root_dir = "/data/datasets"
let userdatasets_root_dir = "/data/userdatasets/"
predatasets["cifar10"] = {};
predatasets["mnist"] = {};
predatasets["KMNIST"] = {};
predatasets["FashionMNIST"] = {};
predatasets["EMNIST_MNIST"] = {};
predatasets["EMNIST_Letters"] = {};
predatasets["EMNIST_Balanced"] = {};
predatasets["EMNIST_Digits"] = {};
predatasets["dogAndCat"] = {};
predatasets["Chars74K"] = {};
predatasets["Dogs"] = {};
predatasets["Animals"] = {};
predatasets["Fruits360"] = {};
predatasets["Boats"] = {};

predatasets["automl_cifar10"] = {};


predatasets["voc"] = {};
predatasets["coco"] = {};

predatasets["ade20k"] = {};

predatasets["cifar10"].name = "cifar10";
predatasets["cifar10"].records = 60000;
predatasets["cifar10"].num_classes = 10;
predatasets["cifar10"].data_dir = datasets_root_dir + "/cifar10";
predatasets["cifar10"].image_tool = "cv2";
predatasets["cifar10"].input_mode = "BGR";
predatasets["cifar10"].workers = 4;
predatasets["cifar10"].keep_difficult = false;
predatasets["cifar10"].mean_value = [124, 116, 104];


predatasets["mnist"].name = "mnist";
predatasets["mnist"].records = 70000;
predatasets["mnist"].num_classes = 10;
predatasets["mnist"].data_dir = datasets_root_dir + "/mnist";
predatasets["mnist"].image_tool = "cv2";
predatasets["mnist"].input_mode = "BGR";
predatasets["mnist"].workers = 4;
predatasets["mnist"].keep_difficult = false;
predatasets["mnist"].mean_value = [0.1307,0.1307,0.1307];

predatasets["KMNIST"].name = "KMNIST";
predatasets["KMNIST"].records = 70000;
predatasets["KMNIST"].num_classes = 10;
predatasets["KMNIST"].data_dir = datasets_root_dir + "/KMNIST";
predatasets["KMNIST"].image_tool = "cv2";
predatasets["KMNIST"].input_mode = "BGR";
predatasets["KMNIST"].workers = 4;
predatasets["KMNIST"].keep_difficult = false;
predatasets["KMNIST"].mean_value = [0.1918,0.1918,0.1918];

predatasets["FashionMNIST"].name = "FashionMNIST";
predatasets["FashionMNIST"].records = 70000;
predatasets["FashionMNIST"].num_classes = 10;
predatasets["FashionMNIST"].data_dir = datasets_root_dir + "/FashionMNIST";
predatasets["FashionMNIST"].image_tool = "cv2";
predatasets["FashionMNIST"].input_mode = "BGR";
predatasets["FashionMNIST"].workers = 4;
predatasets["FashionMNIST"].keep_difficult = false;
predatasets["FashionMNIST"].mean_value = [0.286,0.286,0.286];

predatasets["EMNIST_MNIST"].name = "EMNIST_MNIST";
predatasets["EMNIST_MNIST"].records = 70000;
predatasets["EMNIST_MNIST"].num_classes = 10;
predatasets["EMNIST_MNIST"].data_dir = datasets_root_dir + "/EMNIST_MNIST";
predatasets["EMNIST_MNIST"].image_tool = "cv2";
predatasets["EMNIST_MNIST"].input_mode = "BGR";
predatasets["EMNIST_MNIST"].workers = 4;
predatasets["EMNIST_MNIST"].keep_difficult = false;
predatasets["EMNIST_MNIST"].mean_value = [0.1733,0.1733,0.1733];

predatasets["EMNIST_Letters"].name = "EMNIST_Letters";
predatasets["EMNIST_Letters"].records = 145600;
predatasets["EMNIST_Letters"].num_classes = 26;
predatasets["EMNIST_Letters"].data_dir = datasets_root_dir + "/EMNIST_Letters";
predatasets["EMNIST_Letters"].image_tool = "cv2";
predatasets["EMNIST_Letters"].input_mode = "BGR";
predatasets["EMNIST_Letters"].workers = 4;
predatasets["EMNIST_Letters"].keep_difficult = false;
predatasets["EMNIST_Letters"].mean_value = [0.1733,0.1733,0.1733];

predatasets["EMNIST_Balanced"].name = "EMNIST_Balanced";
predatasets["EMNIST_Balanced"].records = 131600;
predatasets["EMNIST_Balanced"].num_classes = 47;
predatasets["EMNIST_Balanced"].data_dir = datasets_root_dir + "/EMNIST_Balanced";
predatasets["EMNIST_Balanced"].image_tool = "cv2";
predatasets["EMNIST_Balanced"].input_mode = "BGR";
predatasets["EMNIST_Balanced"].workers = 4;
predatasets["EMNIST_Balanced"].keep_difficult = false;
predatasets["EMNIST_Balanced"].mean_value = [0.1751,0.1751,0.1751];

predatasets["EMNIST_Digits"].name = "EMNIST_Digits";
predatasets["EMNIST_Digits"].records = 280000;
predatasets["EMNIST_Digits"].num_classes = 10;
predatasets["EMNIST_Digits"].data_dir = datasets_root_dir + "/EMNIST_Digits";
predatasets["EMNIST_Digits"].image_tool = "cv2";
predatasets["EMNIST_Digits"].input_mode = "BGR";
predatasets["EMNIST_Digits"].workers = 4;
predatasets["EMNIST_Digits"].keep_difficult = false;
predatasets["EMNIST_Digits"].mean_value = [0.1722,0.1722,0.1722];

predatasets["dogAndCat"].name = "dogAndCat";
predatasets["dogAndCat"].records = 25000;
predatasets["dogAndCat"].num_classes = 2;
predatasets["dogAndCat"].data_dir = datasets_root_dir + "/dogAndCat";
predatasets["dogAndCat"].image_tool = "cv2";
predatasets["dogAndCat"].input_mode = "BGR";
predatasets["dogAndCat"].workers = 4;
predatasets["dogAndCat"].keep_difficult = false;
predatasets["dogAndCat"].mean_value = [124, 116, 104];

predatasets["Chars74K"].name = "Chars74K";
predatasets["Chars74K"].records = 7705;
predatasets["Chars74K"].num_classes = 62;
predatasets["Chars74K"].data_dir = datasets_root_dir + "/Chars74K";
predatasets["Chars74K"].image_tool = "cv2";
predatasets["Chars74K"].input_mode = "BGR";
predatasets["Chars74K"].workers = 4;
predatasets["Chars74K"].keep_difficult = false;
predatasets["Chars74K"].mean_value = [0.1307,0.1307,0.1307];

predatasets["Dogs"].name = "Dogs";
predatasets["Dogs"].records = 20580;
predatasets["Dogs"].num_classes = 120;
predatasets["Dogs"].data_dir = datasets_root_dir + "/Dogs";
predatasets["Dogs"].image_tool = "cv2";
predatasets["Dogs"].input_mode = "BGR";
predatasets["Dogs"].workers = 4;
predatasets["Dogs"].keep_difficult = false;
predatasets["Dogs"].mean_value = [0.1307,0.1307,0.1307];

predatasets["Animals"].name = "Animals";
predatasets["Animals"].records = 1740;
predatasets["Animals"].num_classes = 19;
predatasets["Animals"].data_dir = datasets_root_dir + "/Animals";
predatasets["Animals"].image_tool = "cv2";
predatasets["Animals"].input_mode = "BGR";
predatasets["Animals"].workers = 4;
predatasets["Animals"].keep_difficult = false;
predatasets["Animals"].mean_value = [0.1307,0.1307,0.1307];

predatasets["Fruits360"].name = "Fruits360";
predatasets["Fruits360"].records = 69905;
predatasets["Fruits360"].num_classes = 101;
predatasets["Fruits360"].data_dir = datasets_root_dir + "/Fruits360";
predatasets["Fruits360"].image_tool = "cv2";
predatasets["Fruits360"].input_mode = "BGR";
predatasets["Fruits360"].workers = 4;
predatasets["Fruits360"].keep_difficult = false;
predatasets["Fruits360"].mean_value = [0.1307,0.1307,0.1307];

predatasets["Boats"].name = "Boats";
predatasets["Boats"].records = 1460;
predatasets["Boats"].num_classes = 9;
predatasets["Boats"].data_dir = datasets_root_dir + "/Boats";
predatasets["Boats"].image_tool = "cv2";
predatasets["Boats"].input_mode = "BGR";
predatasets["Boats"].workers = 4;
predatasets["Boats"].keep_difficult = false;
predatasets["Boats"].mean_value = [0.1307,0.1307,0.1307];



predatasets["voc"].name = "voc";
predatasets["voc"].records = 800000;
predatasets["voc"].num_classes = 21;
predatasets["voc"].data_dir = datasets_root_dir + "/VOC07+12_DET";
predatasets["voc"].image_tool = "cv2";
predatasets["voc"].input_mode = "BGR";
predatasets["voc"].workers = 4;
predatasets["voc"].keep_difficult = false;
predatasets["voc"].mean_value = [104, 117, 123];



predatasets["coco"].name = "coco";
predatasets["coco"].records = 900000;
predatasets["coco"].num_classes = 10;
predatasets["coco"].data_dir = datasets_root_dir + "/COCO_INS_2014";
predatasets["coco"].image_tool = "cv2";
predatasets["coco"].input_mode = "BGR";
predatasets["coco"].workers = 4;
predatasets["coco"].keep_difficult = false;
predatasets["coco"].mean_value = [124, 116, 104];

predatasets["ade20k"].name = "ade20k";
predatasets["ade20k"].records = 20210;
predatasets["ade20k"].num_classes = 150;
predatasets["ade20k"].data_dir = datasets_root_dir + "/ade20k";
predatasets["ade20k"].image_tool = "cv2";
predatasets["ade20k"].input_mode = "BGR";
predatasets["ade20k"].workers = 8;
predatasets["ade20k"].mean_value = [103, 116, 123];

predatasets["automl_cifar10"].name = "cifar10";
predatasets["automl_cifar10"].records = 60000;
predatasets["automl_cifar10"].num_classes = 10;
predatasets["automl_cifar10"].data_dir = datasets_root_dir + "/cifar10_orig";
predatasets["automl_cifar10"].image_tool = "cv2";
predatasets["automl_cifar10"].input_mode = "BGR";
predatasets["automl_cifar10"].workers = 4;
predatasets["automl_cifar10"].mean_value = [124, 116, 104];





let normalize = [];
normalize["cifar10"] = {};
normalize["mnist"] = {};
normalize["KMNIST"] = {};
normalize["FashionMNIST"] = {};
normalize["EMNIST_MNIST"] = {};
normalize["EMNIST_Letters"] = {};
normalize["EMNIST_Balanced"] = {};
normalize["EMNIST_Digits"] = {};
normalize["Chars74K"] = {};
normalize["Dogs"] = {};
normalize["Animals"] = {};
normalize["Fruits360"] = {};
normalize["Boats"] = {};
normalize["dogAndCat"] = {};
normalize["voc"] = {};
normalize["coco"] = {};
normalize["ade20k"] = {};

normalize["cifar10"].div_value = 1;
normalize["cifar10"].mean = [0.485, 0.456, 0.406];
normalize["cifar10"].std = [0.229, 0.224, 0.225];

normalize["mnist"].div_value = 1;
normalize["mnist"].mean = [0.1307,0.1307,0.1307];
normalize["mnist"].std = [0.3081,0.3081,0.3081];

normalize["KMNIST"].div_value = 1;
normalize["KMNIST"].mean = [0.1918,0.1918,0.1918];
normalize["KMNIST"].std = [0.3483,0.3483,0.3483];

normalize["FashionMNIST"].div_value = 1;
normalize["FashionMNIST"].mean = [0.286,0.286,0.286];
normalize["FashionMNIST"].std = [0.353,0.353,0.353];

normalize["EMNIST_MNIST"].div_value = 1;
normalize["EMNIST_MNIST"].mean = [0.1733,0.1733,0.1733];
normalize["EMNIST_MNIST"].std = [0.3317,0.3317,0.3317];

normalize["EMNIST_Letters"].div_value = 1;
normalize["EMNIST_Letters"].mean = [0.1733,0.1733,0.1733];
normalize["EMNIST_Letters"].std = [0.3317,0.3317,0.3317];

normalize["EMNIST_Balanced"].div_value = 1;
normalize["EMNIST_Balanced"].mean = [0.1751,0.1751,0.1751];
normalize["EMNIST_Balanced"].std = [0.3332,0.3332,0.3332];

normalize["EMNIST_Digits"].div_value = 1;
normalize["EMNIST_Digits"].mean = [0.1722,0.1722,0.1722];
normalize["EMNIST_Digits"].std = [0.3309,0.3332,0.3332];


normalize["dogAndCat"].div_value = 255;
normalize["dogAndCat"].mean = [0.485, 0.456, 0.406];
normalize["dogAndCat"].std = [0.485, 0.456, 0.406];

normalize["Chars74K"].div_value = 1;
normalize["Chars74K"].mean = [0.1307,0.1307,0.1307];
normalize["Chars74K"].std = [0.3081,0.3081,0.3081];

normalize["Dogs"].div_value = 255;
normalize["Dogs"].mean = [0.485, 0.456, 0.406];
normalize["Dogs"].std = [0.485, 0.456, 0.406];

normalize["Animals"].div_value = 255;
normalize["Animals"].mean = [0.485, 0.456, 0.406];
normalize["Animals"].std = [0.485, 0.456, 0.406];

normalize["Fruits360"].div_value = 255;
normalize["Fruits360"].mean = [0.485, 0.456, 0.406];
normalize["Fruits360"].std = [0.485, 0.456, 0.406];

normalize["Boats"].div_value = 255;
normalize["Boats"].mean = [0.485, 0.456, 0.406];
normalize["Boats"].std = [0.485, 0.456, 0.406];

normalize["voc"].div_value = 255;
normalize["voc"].mean = [104.0, 117.0, 123.0];
normalize["voc"].std = [1.0, 1.0, 1.0];

normalize["coco"].div_value = 1;
normalize["coco"].mean = [0.485, 0.456, 0.406];
normalize["coco"].std = [0.229, 0.224, 0.225];

normalize["ade20k"].div_value = 255;
normalize["ade20k"].mean = [102.9801, 115.9465, 122.7717];
normalize["ade20k"].std = [1.0, 1.0, 1.0];


predatasets["cifar10"].normalize = normalize["cifar10"];
predatasets["mnist"].normalize = normalize["mnist"];
predatasets["KMNIST"].normalize = normalize["KMNIST"];
predatasets["FashionMNIST"].normalize = normalize["FashionMNIST"];
predatasets["EMNIST_MNIST"].normalize = normalize["EMNIST_MNIST"];
predatasets["EMNIST_Letters"].normalize = normalize["EMNIST_Letters"];
predatasets["EMNIST_Balanced"].normalize = normalize["EMNIST_Balanced"];
predatasets["EMNIST_Digits"].normalize = normalize["EMNIST_Digits"];
predatasets["dogAndCat"].normalize = normalize["dogAndCat"];
predatasets["Chars74K"].normalize = normalize["Chars74K"];
predatasets["Dogs"].normalize = normalize["Dogs"];
predatasets["Animals"].normalize = normalize["Animals"];
predatasets["Fruits360"].normalize = normalize["Fruits360"];
predatasets["Boats"].normalize = normalize["Boats"];


predatasets["voc"].normalize = normalize["voc"];
predatasets["coco"].normalize = normalize["coco"];
predatasets["ade20k"].normalize = normalize["ade20k"];
predatasets["automl_cifar10"].normalize = normalize["cifar10"];




let details = [];
details["cifar10"] = {};
details["mnist"] = {};
details["KMNIST"] = {};
details["FashionMNIST"] = {};
details["EMNIST_MNIST"] = {};
details["EMNIST_Letters"] = {};
details["EMNIST_Balanced"] = {};
details["EMNIST_Digits"] = {};
details["Chars74K"] = {};
details["Dogs"] = {};
details["Animals"] = {};
details["Fruits360"] = {};
details["Boats"] = {};

details["dogAndCat"] = {};
details["voc"] = {};
details["coco"] = {};
details["ade20k"] = {};
details["automl_cifar10"] = {};



details["cifar10"].name_seq = ["plane", "car", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"];
details["cifar10"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["mnist"].name_seq = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
details["mnist"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["KMNIST"].name_seq = ["お", "き", "す", "つ", "な", "は", "ま", "や", "れ", "を"];
details["KMNIST"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["FashionMNIST"].name_seq = ["Top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"];
details["FashionMNIST"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["EMNIST_MNIST"].name_seq = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
details["EMNIST_MNIST"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["EMNIST_Letters"].name_seq = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"];
details["EMNIST_Letters"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["EMNIST_Balanced"].name_seq = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9","A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z","a","b","d","e","f","g","h","n","q","r","t"];
details["EMNIST_Balanced"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["EMNIST_Digits"].name_seq = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
details["EMNIST_Digits"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["Chars74K"].name_seq = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9","A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z","a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
details["Chars74K"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85],[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85],[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];


details["dogAndCat"].name_seq = ["dog", "cat"];
details["dogAndCat"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["Dogs"].name_seq = ['Chihuahua', 'Japanese_spaniel', 'Maltese_dog', 'Pekinese', 'Shih-Tzu', 'Blenheim_spaniel', 'papillon', 'toy_terrier', 'Rhodesian_ridgeback', 'Afghan_hound', 'basset', 'beagle', 'bloodhound', 'bluetick', 'black-and-tan_coonhound', 'Walker_hound', 'redbone', 'borzoi', 'Irish_wolfhound', 'Italian_greyhound', 'whippet', 'Ibizan_hound', 'Norwegian_elkhound', 'Saluki', 'Scottish_deerhound', 'Weimaraner', 'Staffordshire_bullterrier', 'American_Staffordshire_terrier', 'Bedlington_terrier', 'Border_terrier', 'Kerry_blue_terrier', 'Irish_terrier', 'Norfolk_terrier', 'Norwich_terrier', 'Yorkshire_terrier', 'wire-haired_fox_terrier', 'Lakeland_terrier', 'Sealyham_terrier', 'Airedale', 'cairn', 'Australian_terrier', 'Dandie_Dinmont', 'Boston_bull', 'miniature_schnauzer', 'giant_schnauzer', 'standard_schnauzer', 'Scotch_terrier', 'Tibetan_terrier', 'silky_terrier', 'soft-coated_wheaten_terrier', 'West_Highland_white_terrier', 'Lhasa', 'flat-coated_retriever', 'curly-coated_retriever', 'golden_retriever', 'Labrador_retriever', 'Chesapeake_Bay_retriever', 'German_short-haired_pointer', 'vizsla', 'English_setter', 'Irish_setter', 'Gordon_setter', 'Brittany_spaniel', 'clumber', 'English_springer', 'Welsh_springer_spaniel', 'cocker_spaniel', 'Sussex_spaniel', 'Irish_water_spaniel', 'kuvasz', 'schipperke', 'groenendael', 'malinois', 'briard', 'kelpie', 'komondor', 'Old_English_sheepdog', 'collie', 'Border_collie', 'Bouvier_des_Flandres', 'Rottweiler', 'German_shepherd', 'Doberman', 'miniature_pinscher', 'Greater_Swiss_Mountain_dog', 'Bernese_mountain_dog', 'Appenzeller', 'EntleBucher', 'boxer', 'bull_mastiff', 'Tibetan_mastiff', 'Great_Dane', 'Saint_Bernard', 'Eskimo_dog', 'malamute', 'Siberian_husky', 'affenpinscher', 'basenji', 'pug', 'Leonberg', 'Newfoundland', 'Great_Pyrenees', 'Samoyed', 'Pomeranian', 'chow', 'keeshond', 'Brabancon_griffon', 'Pembroke', 'Cardigan', 'toy_poodle', 'miniature_poodle', 'standard_poodle', 'Mexican_hairless', 'dingo', 'dhole', 'African_hunting_dog', 'English_foxhound', 'otterhound', 'Shetland_sheepdog', 'French_bulldog'];
details["Dogs"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["Animals"].name_seq = ['bear','cougar','cow','coyote','deer','elephant','giraffe','goat','gorilla','horse','kangaroo','leopard','lion','panda','penquin','sheep','skunk','tiger','zebra'];
details["Animals"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

details["Fruits360"].name_seq = ['Apple Braeburn','Apple Crimson Snow','Apple Golden 1','Apple Golden 2','Apple Golden 3','Apple Granny Smith','Apple Red 1','Apple Red 2','Apple Red 3','Apple Red Delicious','Apple Red Yellow 1','Apple Red Yellow 2','Apricot','Avocado','Avocado ripe','Banana','Banana Lady Finger','Banana Red','Cactus fruit','Cantaloupe 1','Cantaloupe 2','Carambula','Cherry 1','Cherry 2','Cherry Rainier','Cherry Wax Black','Cherry Wax Red','Cherry Wax Yellow','Chestnut','Clementine','Cocos','Dates','Granadilla','Grape Blue','Grape Pink','Grape White','Grape White 2','Grape White 3','Grape White 4','Grapefruit Pink','Grapefruit White','Guava','Hazelnut','Huckleberry','Kaki','Kiwi','Kohlrabi','Kumquats','Lemon','Lemon Meyer','Limes','Lychee','Mandarine','Mango','Mangostan','Maracuja','Melon Piel de Sapo','Mulberry','Nectarine','Orange','Papaya','Passion Fruit','Peach','Peach 2','Peach Flat','Pear','Pear Abate','Pear Kaiser','Pear Monster','Pear Red','Pear Williams','Pepino','Pepper Green','Pepper Red','Pepper Yellow','Physalis','Physalis with Husk','Pineapple','Pineapple Mini','Pitahaya Red','Plum','Plum 2','Plum 3','Pomegranate','Pomelo Sweetie','Quince','Rambutan','Raspberry','Redcurrant','Salak','Strawberry','Strawberry Wedge','Tamarillo','Tangelo','Tomato 1','Tomato 2','Tomato 3','Tomato 4','Tomato Cherry Red','Tomato Maroon','Walnut'];
details["Fruits360"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];


details["Boats"].name_seq = ['buoy','cruise ship','ferry boat','freight boat','gondola','inflatable boat','kayak','paper boat','sailboat'];
details["Boats"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];



details["ade20k"].color_list = [[128, 64, 128], [244, 35, 232], [70, 70, 70], [102, 102, 156], [190, 153, 153],[153, 153, 153], [250, 170, 30], [220, 220, 0], [107, 142, 35], [152, 251, 152],
[70, 130, 180], [220, 20, 60], [255, 0, 0], [0, 0, 142], [0, 0, 70], [0, 60, 100],
[0, 80, 100], [0, 0, 230], [119, 11, 32]];

details["automl_cifar10"].name_seq = ["plane", "car", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"];
details["automl_cifar10"].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];




details["voc"].color_list = [[255, 170, 30], [0, 0, 70], [244, 35, 232]];
details["voc"].name_id_dict = {
    "aeroplane": 1, "bicycle": 2, "bird": 3, "boat": 4, "bottle": 5, "bus": 6, "car": 7,
    "cat": 8, "chair": 9, "cow": 10, "diningtable": 11, "dog": 12, "horse": 13, "motorbike": 14,
    "person": 15, "pottedplant": 16, "sheep": 17, "sofa": 18, "train": 19, "tvmonitor": 20
  };
details["voc"].name_seq = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair","cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant","sheep", "sofa", "train", "tvmonitor"];


details["coco"].color_list = [[255, 170, 30], [255, 0, 0], [0, 255, 0], [0, 0, 255]];
details["coco"].coco_cat_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21,
    22, 23, 24, 25, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
    43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
    62, 63, 64, 65, 67, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84,
    85, 86, 87, 88, 89, 90];
details["coco"].name_seq = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
"truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter",
"bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant",
"bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie",
"suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
"baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
"bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
"banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog",
"pizza", "donut", "cake", "chair", "couch", "potted plant", "bed",
"dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
"cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
"book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"];
details["coco"].name_id_dict = {
    "person": 1, "bicycle":2, "car": 3, "motorcycle": 4, "airplane": 5, "bus": 6, "train": 7,
    "truck": 8, "boat": 9, "traffic light": 10, "fire hydrant": 11, "stop sign": 12, "parking meter": 13,
    "bench": 14, "bird": 15, "cat": 16, "dog": 17, "horse": 18, "sheep": 19, "cow": 20, "elephant": 21,
    "bear": 22, "zebra": 23, "giraffe": 24, "backpack": 25, "umbrella": 26, "handbag": 27, "tie": 28,
    "suitcase": 29, "frisbee": 30, "skis": 31, "snowboard": 32, "sports ball": 33, "kite": 34,
    "baseball bat": 35, "baseball glove": 36, "skateboard": 37, "surfboard": 38, "tennis racket": 39,
    "bottle": 40, "wine glass": 41, "cup": 42, "fork": 43, "knife": 44, "spoon": 45, "bowl": 46,
    "banana": 47, "apple": 48, "sandwich": 49, "orange": 50, "broccoli": 51, "carrot": 52, "hot dog": 53,
    "pizza": 54, "donut": 55, "cake": 56, "chair": 57, "couch": 58, "potted plant": 59, "bed": 60,
    "dining table": 61, "toilet": 62, "tv": 63, "laptop": 64, "mouse": 65, "remote": 66, "keyboard": 67,
    "cell phone": 68, "microwave": 69, "oven": 70, "toaster": 71, "sink": 72, "refrigerator": 73,
    "book": 74, "clock": 75, "vase": 76, "scissors": 77, "teddy bear": 78, "hair drier": 79, "toothbrush": 80
  };





detloss = ["SSD MultiBox:ssd_multibox_loss","Yolo:yolov3_det_loss"];
clsloss = ["FC:fc_ce_loss"];
segloss = ["FS:fs_auxce_loss"];

let dataset_params = [];
dataset_params["cifar10"] = {};
dataset_params["cifar10"].dataset_train_batchsize=128;
dataset_params["cifar10"].dataset_train_sizemode="fix_size";
dataset_params["cifar10"].dataset_train_inputsize=32;
dataset_params["cifar10"].dataset_train_align_method="only_pad";
dataset_params["cifar10"].dataset_val_batchsize=128;
dataset_params["cifar10"].dataset_val_sizemode="fix_size";
dataset_params["cifar10"].dataset_val_inputsize=32;
dataset_params["cifar10"].dataset_val_align_method="only_pad";
dataset_params["cifar10"].dataset_test_batchsize=128;
dataset_params["cifar10"].dataset_test_sizemode="fix_size";
dataset_params["cifar10"].dataset_test_inputsize=32;
dataset_params["cifar10"].dataset_test_align_method="only_pad";

dataset_params["mnist"] = {};
dataset_params["mnist"].dataset_train_batchsize=128;
dataset_params["mnist"].dataset_train_sizemode="fix_size";
dataset_params["mnist"].dataset_train_inputsize=28;
dataset_params["mnist"].dataset_train_align_method="only_pad";
dataset_params["mnist"].dataset_val_batchsize=128;
dataset_params["mnist"].dataset_val_sizemode="fix_size";
dataset_params["mnist"].dataset_val_inputsize=28;
dataset_params["mnist"].dataset_val_align_method="only_pad";
dataset_params["mnist"].dataset_test_batchsize=128;
dataset_params["mnist"].dataset_test_sizemode="fix_size";
dataset_params["mnist"].dataset_test_inputsize=28;
dataset_params["mnist"].dataset_test_align_method="only_pad";

dataset_params["KMNIST"] = {};
dataset_params["KMNIST"].dataset_train_batchsize=128;
dataset_params["KMNIST"].dataset_train_sizemode="fix_size";
dataset_params["KMNIST"].dataset_train_inputsize=28;
dataset_params["KMNIST"].dataset_train_align_method="only_pad";
dataset_params["KMNIST"].dataset_val_batchsize=128;
dataset_params["KMNIST"].dataset_val_sizemode="fix_size";
dataset_params["KMNIST"].dataset_val_inputsize=28;
dataset_params["KMNIST"].dataset_val_align_method="only_pad";
dataset_params["KMNIST"].dataset_test_batchsize=128;
dataset_params["KMNIST"].dataset_test_sizemode="fix_size";
dataset_params["KMNIST"].dataset_test_inputsize=28;
dataset_params["KMNIST"].dataset_test_align_method="only_pad";

dataset_params["FashionMNIST"] = {};
dataset_params["FashionMNIST"].dataset_train_batchsize=128;
dataset_params["FashionMNIST"].dataset_train_sizemode="fix_size";
dataset_params["FashionMNIST"].dataset_train_inputsize=28;
dataset_params["FashionMNIST"].dataset_train_align_method="only_pad";
dataset_params["FashionMNIST"].dataset_val_batchsize=128;
dataset_params["FashionMNIST"].dataset_val_sizemode="fix_size";
dataset_params["FashionMNIST"].dataset_val_inputsize=28;
dataset_params["FashionMNIST"].dataset_val_align_method="only_pad";
dataset_params["FashionMNIST"].dataset_test_batchsize=128;
dataset_params["FashionMNIST"].dataset_test_sizemode="fix_size";
dataset_params["FashionMNIST"].dataset_test_inputsize=28;
dataset_params["FashionMNIST"].dataset_test_align_method="only_pad";

dataset_params["EMNIST_MNIST"] = {};
dataset_params["EMNIST_MNIST"].dataset_train_batchsize=128;
dataset_params["EMNIST_MNIST"].dataset_train_sizemode="fix_size";
dataset_params["EMNIST_MNIST"].dataset_train_inputsize=28;
dataset_params["EMNIST_MNIST"].dataset_train_align_method="only_pad";
dataset_params["EMNIST_MNIST"].dataset_val_batchsize=128;
dataset_params["EMNIST_MNIST"].dataset_val_sizemode="fix_size";
dataset_params["EMNIST_MNIST"].dataset_val_inputsize=28;
dataset_params["EMNIST_MNIST"].dataset_val_align_method="only_pad";
dataset_params["EMNIST_MNIST"].dataset_test_batchsize=128;
dataset_params["EMNIST_MNIST"].dataset_test_sizemode="fix_size";
dataset_params["EMNIST_MNIST"].dataset_test_inputsize=28;
dataset_params["EMNIST_MNIST"].dataset_test_align_method="only_pad";

dataset_params["EMNIST_Balanced"] = {};
dataset_params["EMNIST_Balanced"].dataset_train_batchsize=128;
dataset_params["EMNIST_Balanced"].dataset_train_sizemode="fix_size";
dataset_params["EMNIST_Balanced"].dataset_train_inputsize=28;
dataset_params["EMNIST_Balanced"].dataset_train_align_method="only_pad";
dataset_params["EMNIST_Balanced"].dataset_val_batchsize=128;
dataset_params["EMNIST_Balanced"].dataset_val_sizemode="fix_size";
dataset_params["EMNIST_Balanced"].dataset_val_inputsize=28;
dataset_params["EMNIST_Balanced"].dataset_val_align_method="only_pad";
dataset_params["EMNIST_Balanced"].dataset_test_batchsize=128;
dataset_params["EMNIST_Balanced"].dataset_test_sizemode="fix_size";
dataset_params["EMNIST_Balanced"].dataset_test_inputsize=28;
dataset_params["EMNIST_Balanced"].dataset_test_align_method="only_pad";

dataset_params["EMNIST_Letters"] = {};
dataset_params["EMNIST_Letters"].dataset_train_batchsize=128;
dataset_params["EMNIST_Letters"].dataset_train_sizemode="fix_size";
dataset_params["EMNIST_Letters"].dataset_train_inputsize=28;
dataset_params["EMNIST_Letters"].dataset_train_align_method="only_pad";
dataset_params["EMNIST_Letters"].dataset_val_batchsize=128;
dataset_params["EMNIST_Letters"].dataset_val_sizemode="fix_size";
dataset_params["EMNIST_Letters"].dataset_val_inputsize=28;
dataset_params["EMNIST_Letters"].dataset_val_align_method="only_pad";
dataset_params["EMNIST_Letters"].dataset_test_batchsize=128;
dataset_params["EMNIST_Letters"].dataset_test_sizemode="fix_size";
dataset_params["EMNIST_Letters"].dataset_test_inputsize=28;
dataset_params["EMNIST_Letters"].dataset_test_align_method="only_pad";

dataset_params["EMNIST_Digits"] = {};
dataset_params["EMNIST_Digits"].dataset_train_batchsize=128;
dataset_params["EMNIST_Digits"].dataset_train_sizemode="fix_size";
dataset_params["EMNIST_Digits"].dataset_train_inputsize=28;
dataset_params["EMNIST_Digits"].dataset_train_align_method="only_pad";
dataset_params["EMNIST_Digits"].dataset_val_batchsize=128;
dataset_params["EMNIST_Digits"].dataset_val_sizemode="fix_size";
dataset_params["EMNIST_Digits"].dataset_val_inputsize=28;
dataset_params["EMNIST_Digits"].dataset_val_align_method="only_pad";
dataset_params["EMNIST_Digits"].dataset_test_batchsize=128;
dataset_params["EMNIST_Digits"].dataset_test_sizemode="fix_size";
dataset_params["EMNIST_Digits"].dataset_test_inputsize=28;
dataset_params["EMNIST_Digits"].dataset_test_align_method="only_pad";

dataset_params["dogAndCat"] = {};
dataset_params["dogAndCat"].dataset_train_batchsize=128;
dataset_params["dogAndCat"].dataset_train_sizemode="fix_size";
dataset_params["dogAndCat"].dataset_train_inputsize=224;
dataset_params["dogAndCat"].dataset_train_align_method="only_pad";
dataset_params["dogAndCat"].dataset_val_batchsize=128;
dataset_params["dogAndCat"].dataset_val_sizemode="fix_size";
dataset_params["dogAndCat"].dataset_val_inputsize=224;
dataset_params["dogAndCat"].dataset_val_align_method="only_pad";
dataset_params["dogAndCat"].dataset_test_batchsize=128;
dataset_params["dogAndCat"].dataset_test_sizemode="fix_size";
dataset_params["dogAndCat"].dataset_test_inputsize=224;
dataset_params["dogAndCat"].dataset_test_align_method="only_pad";


dataset_params["Dogs"] = {};
dataset_params["Dogs"].dataset_train_batchsize=128;
dataset_params["Dogs"].dataset_train_sizemode="fix_size";
dataset_params["Dogs"].dataset_train_inputsize=96;
dataset_params["Dogs"].dataset_train_align_method="scale_and_pad";
dataset_params["Dogs"].dataset_val_batchsize=128;
dataset_params["Dogs"].dataset_val_sizemode="fix_size";
dataset_params["Dogs"].dataset_val_inputsize=96;
dataset_params["Dogs"].dataset_val_align_method="scale_and_pad";
dataset_params["Dogs"].dataset_test_batchsize=128;
dataset_params["Dogs"].dataset_test_sizemode="fix_size";
dataset_params["Dogs"].dataset_test_inputsize=96;
dataset_params["Dogs"].dataset_test_align_method="scale_and_pad";

dataset_params["Animals"] = {};
dataset_params["Animals"].dataset_train_batchsize=128;
dataset_params["Animals"].dataset_train_sizemode="fix_size";
dataset_params["Animals"].dataset_train_inputsize=96;
dataset_params["Animals"].dataset_train_align_method="scale_and_pad";
dataset_params["Animals"].dataset_val_batchsize=128;
dataset_params["Animals"].dataset_val_sizemode="fix_size";
dataset_params["Animals"].dataset_val_inputsize=96;
dataset_params["Animals"].dataset_val_align_method="scale_and_pad";
dataset_params["Animals"].dataset_test_batchsize=128;
dataset_params["Animals"].dataset_test_sizemode="fix_size";
dataset_params["Animals"].dataset_test_inputsize=96;
dataset_params["Animals"].dataset_test_align_method="scale_and_pad";

dataset_params["Chars74K"] = {};
dataset_params["Chars74K"].dataset_train_batchsize=128;
dataset_params["Chars74K"].dataset_train_sizemode="fix_size";
dataset_params["Chars74K"].dataset_train_inputsize=32;
dataset_params["Chars74K"].dataset_train_align_method="scale_and_pad";
dataset_params["Chars74K"].dataset_val_batchsize=128;
dataset_params["Chars74K"].dataset_val_sizemode="fix_size";
dataset_params["Chars74K"].dataset_val_inputsize=32;
dataset_params["Chars74K"].dataset_val_align_method="scale_and_pad";
dataset_params["Chars74K"].dataset_test_batchsize=128;
dataset_params["Chars74K"].dataset_test_sizemode="fix_size";
dataset_params["Chars74K"].dataset_test_inputsize=32;
dataset_params["Chars74K"].dataset_test_align_method="scale_and_pad";

dataset_params["Fruits360"] = {};
dataset_params["Fruits360"].dataset_train_batchsize=128;
dataset_params["Fruits360"].dataset_train_sizemode="fix_size";
dataset_params["Fruits360"].dataset_train_inputsize=32;
dataset_params["Fruits360"].dataset_train_align_method="scale_and_pad";
dataset_params["Fruits360"].dataset_val_batchsize=128;
dataset_params["Fruits360"].dataset_val_sizemode="fix_size";
dataset_params["Fruits360"].dataset_val_inputsize=32;
dataset_params["Fruits360"].dataset_val_align_method="scale_and_pad";
dataset_params["Fruits360"].dataset_test_batchsize=128;
dataset_params["Fruits360"].dataset_test_sizemode="fix_size";
dataset_params["Fruits360"].dataset_test_inputsize=32;
dataset_params["Fruits360"].dataset_test_align_method="scale_and_pad";

dataset_params["Boats"] = {};
dataset_params["Boats"].dataset_train_batchsize=32;
dataset_params["Boats"].dataset_train_sizemode="fix_size";
dataset_params["Boats"].dataset_train_inputsize=64;
dataset_params["Boats"].dataset_train_align_method="scale_and_pad";
dataset_params["Boats"].dataset_val_batchsize=32;
dataset_params["Boats"].dataset_val_sizemode="fix_size";
dataset_params["Boats"].dataset_val_inputsize=64;
dataset_params["Boats"].dataset_val_align_method="scale_and_pad";
dataset_params["Boats"].dataset_test_batchsize=32;
dataset_params["Boats"].dataset_test_sizemode="fix_size";
dataset_params["Boats"].dataset_test_inputsize=64;
dataset_params["Boats"].dataset_test_align_method="scale_and_pad";

dataset_params["voc"] = {};
dataset_params["voc"].dataset_train_batchsize=32;
dataset_params["voc"].dataset_train_sizemode="fix_size";
dataset_params["voc"].dataset_train_inputsize=300;
dataset_params["voc"].dataset_train_align_method="only_scale";
dataset_params["voc"].dataset_val_batchsize=32;
dataset_params["voc"].dataset_val_sizemode="fix_size";
dataset_params["voc"].dataset_val_inputsize=300;
dataset_params["voc"].dataset_val_align_method="only_scale";

dataset_params["coco"] = {};
dataset_params["coco"].dataset_train_batchsize=32;
dataset_params["coco"].dataset_train_sizemode="fix_size";
dataset_params["coco"].dataset_train_inputsize=300;
dataset_params["coco"].dataset_train_align_method="only_scale";
dataset_params["coco"].dataset_val_batchsize=32;
dataset_params["coco"].dataset_val_sizemode="fix_size";
dataset_params["coco"].dataset_val_inputsize=300;
dataset_params["coco"].dataset_val_align_method="only_scale";

dataset_params["ade20k"] = {};
dataset_params["ade20k"].dataset_train_batchsize=4;
dataset_params["ade20k"].dataset_train_sizemode="fix_size";
dataset_params["ade20k"].dataset_train_inputsize=520;
dataset_params["ade20k"].dataset_train_align_method="only_pad";
dataset_params["ade20k"].dataset_val_batchsize=1;
dataset_params["ade20k"].dataset_val_sizemode="max_size";
dataset_params["ade20k"].dataset_val_inputsize=300;
dataset_params["ade20k"].dataset_val_align_method="only_pad";
dataset_params["ade20k"].dataset_reduce_zero_label = 'true';



dataset_params["automl_cifar10"] = {};
dataset_params["automl_cifar10"].dataset_search_train_batchsize=64;
dataset_params["automl_cifar10"].dataset_search_val_batchsize=64;
dataset_params["automl_cifar10"].dataset_search_test_batchsize=64;
dataset_params["automl_cifar10"].dataset_finetune_train_batchsize=64;
dataset_params["automl_cifar10"].dataset_finetune_val_batchsize=64;
dataset_params["automl_cifar10"].dataset_finetune_test_batchsize=64;
dataset_params["automl_cifar10"].dataset_search_cutout='false';
dataset_params["automl_cifar10"].dataset_search_cutout_length=16;
dataset_params["automl_cifar10"].dataset_finetune_cutout='false';
dataset_params["automl_cifar10"].dataset_finetune_cutout_length=16;


hyper_params = [];
hyper_params["single_shot_detector"] = {};
hyper_params["single_shot_detector"].hparamter_metric = "epoch";
hyper_params["single_shot_detector"].hparamter_base_lr = 0.0004;
hyper_params["single_shot_detector"].hparamter_lr_policy = "step";
hyper_params["single_shot_detector"].hparamter_gamma = 0.1;
hyper_params["single_shot_detector"].hparamter_step_value = "156,195,234";
hyper_params["single_shot_detector"].solver_display_iter = 20;
hyper_params["single_shot_detector"].solver_test_interval = 40;
hyper_params["single_shot_detector"].solver_max_epoch = 235;
hyper_params["single_shot_detector"].optim_method = "adam";
hyper_params["single_shot_detector"].optim_adam_betas = "0.9,0.999";
hyper_params["single_shot_detector"].optim_adam_eps = 1e-08;
hyper_params["single_shot_detector"].optim_adam_weight_decay = 0.0001;
hyper_params["single_shot_detector"].optim_sgd_weight_decay = 0.0005;
hyper_params["single_shot_detector"].optim_sgd_momentum = 0.9;
hyper_params["single_shot_detector"].optim_sgd_nesterov = false;
hyper_params["single_shot_detector"].optim_iswarm = true;
hyper_params["single_shot_detector"].optim_warmiters = 200;
hyper_params["single_shot_detector"].hparamter_loss_type = "ssd_multibox_loss";
hyper_params["single_shot_detector"].hparamter_nms_mode = "union";
hyper_params["single_shot_detector"].hparamter_nms_max_threshold = 0.45;
hyper_params["single_shot_detector"].hparamter_nms_pre = 1000;
hyper_params["single_shot_detector"].hparamter_res_val_conf_thre = 0.01;
hyper_params["single_shot_detector"].hparamter_res_vis_conf_thre = 0.5;
hyper_params["single_shot_detector"].hparamter_res_max_per_image = 200;
hyper_params["single_shot_detector"].hparamter_res_cls_keep_num = 50;

hyper_params["yolov3"] = {};
hyper_params["yolov3"].hparamter_metric = "epoch";
hyper_params["yolov3"].hparamter_base_lr = 0.0004;
hyper_params["yolov3"].hparamter_lr_policy = "step";
hyper_params["yolov3"].hparamter_gamma = 0.1;
hyper_params["yolov3"].hparamter_step_value = "156,195,234";
hyper_params["yolov3"].solver_display_iter = 20;
hyper_params["yolov3"].solver_test_interval = 40;
hyper_params["yolov3"].solver_max_epoch = 235;
hyper_params["yolov3"].optim_method = "adam";
hyper_params["yolov3"].optim_adam_betas = "0.9,0.999";
hyper_params["yolov3"].optim_adam_eps = 1e-08;
hyper_params["yolov3"].optim_adam_weight_decay = 0.0001;
hyper_params["yolov3"].optim_sgd_weight_decay = 0.0005;
hyper_params["yolov3"].optim_sgd_momentum = 0.9;
hyper_params["yolov3"].optim_sgd_nesterov = false;
hyper_params["yolov3"].optim_iswarm = true;
hyper_params["yolov3"].optim_warmiters = 1000;
hyper_params["yolov3"].hparamter_loss_type = "yolov3_det_loss";
hyper_params["yolov3"].hparamter_nms_mode = "union";
hyper_params["yolov3"].hparamter_nms_max_threshold = 0.45;
hyper_params["yolov3"].hparamter_nms_pre = 1000;
hyper_params["yolov3"].hparamter_res_val_conf_thre = 0.5;
hyper_params["yolov3"].hparamter_res_vis_conf_thre = 0.5;
hyper_params["yolov3"].hparamter_res_max_per_image = 200;
hyper_params["yolov3"].hparamter_res_cls_keep_num = 50;


hyper_params["fc_classifier"] = {};
hyper_params["fc_classifier"].hparamter_metric = "epoch";
hyper_params["fc_classifier"].hparamter_base_lr = 0.0001;
hyper_params["fc_classifier"].hparamter_lr_policy = "step";
hyper_params["fc_classifier"].hparamter_gamma = 0.1;
hyper_params["fc_classifier"].hparamter_step_value = "30,40,50";
hyper_params["fc_classifier"].solver_display_iter = 20;
hyper_params["fc_classifier"].solver_test_interval = 50;
hyper_params["fc_classifier"].solver_max_epoch = 60;
hyper_params["fc_classifier"].optim_method = "adam";
hyper_params["fc_classifier"].optim_adam_betas = "0.9,0.999";
hyper_params["fc_classifier"].optim_adam_eps = 1e-08;
hyper_params["fc_classifier"].optim_adam_weight_decay = 0.0001;
hyper_params["fc_classifier"].optim_sgd_weight_decay = 0.00004;
hyper_params["fc_classifier"].optim_sgd_momentum = 0.9;
hyper_params["fc_classifier"].optim_sgd_nesterov = false;
hyper_params["fc_classifier"].optim_iswarm = false;
hyper_params["fc_classifier"].optim_warmiters = 0;
hyper_params["fc_classifier"].hparamter_loss_type = "fc_ce_loss";

hyper_params["fcn_segmentor"] = {};
hyper_params["fcn_segmentor"].hparamter_metric = "iters";
hyper_params["fcn_segmentor"].hparamter_base_lr = 0.02;
hyper_params["fcn_segmentor"].hparamter_lr_policy = "lambda_poly";
hyper_params["fcn_segmentor"].hparamter_gamma = 0.5;
hyper_params["fcn_segmentor"].hparamter_step_value = "100";
hyper_params["fcn_segmentor"].solver_display_iter = 20;
hyper_params["fcn_segmentor"].solver_test_interval = 50;
hyper_params["fcn_segmentor"].solver_max_epoch = 60;
hyper_params["fcn_segmentor"].optim_method = "adam";
hyper_params["fcn_segmentor"].optim_adam_betas = "0.9,0.999";
hyper_params["fcn_segmentor"].optim_adam_eps = 1e-08;
hyper_params["fcn_segmentor"].optim_adam_weight_decay = 0.0001;
hyper_params["fcn_segmentor"].optim_sgd_weight_decay = 0.00004;
hyper_params["fcn_segmentor"].optim_sgd_momentum = 0.9;
hyper_params["fcn_segmentor"].optim_sgd_nesterov = false;
hyper_params["fcn_segmentor"].optim_iswarm = true;
hyper_params["fcn_segmentor"].optim_warmiters = 1000;
hyper_params["fcn_segmentor"].hparamter_loss_type = "fs_auxce_loss";


hyper_params["darts"] = {};
hyper_params["darts"].hparamter_search_metric = "epoch";
hyper_params["darts"].hparamter_search_lr_policy = 'annealing';
hyper_params["darts"].hparamter_search_base_lr = 0.025;
hyper_params["darts"].hparamter_search_lr_min = 0.001;
hyper_params["darts"].hparamter_search_arch_lr = 0.0001;
hyper_params["darts"].hparamter_search_seed = 2;
hyper_params["darts"].hparamter_search_init_ch = 16;
hyper_params["darts"].hparamter_search_layers_num = 8;
hyper_params["darts"].hparamter_search_grad_clip = 5;
hyper_params["darts"].solver_search_display_iter = 200;
hyper_params["darts"].solver_search_test_interval = 1000;
hyper_params["darts"].solver_search_max_epoch = 10;
hyper_params["darts"].optim_search_method = 'sgd';
hyper_params["darts"].optim_search_sgd_weight_decay = 0.00004;
hyper_params["darts"].optim_search_sgd_momentum = 0.9;
hyper_params["darts"].optim_search_sgd_nesterov = false;
hyper_params["darts"].optim_search_sgd_arch_weight_decay = 0.001;
hyper_params["darts"].optim_search_sgd_arch_momentum = 0.001;

hyper_params["darts"].hparamter_finetune_metric = "epoch";
hyper_params["darts"].hparamter_finetune_lr_policy = 'annealing';
hyper_params["darts"].hparamter_finetune_base_lr = 0.025;
hyper_params["darts"].hparamter_finetune_lr_min = 0.001;

hyper_params["darts"].hparamter_finetune_seed = 0;
hyper_params["darts"].hparamter_finetune_init_ch = 36;
hyper_params["darts"].hparamter_finetune_layers_num = 20;
hyper_params["darts"].hparamter_finetune_grad_clip = 5;
hyper_params["darts"].hparamter_finetune_auxiliary = false;
hyper_params["darts"].hparamter_finetune_auxiliary_weight = 0.4;
hyper_params["darts"].hparamter_finetune_drop_path_prob = 0.2;
hyper_params["darts"].solver_finetune_display_iter = 20;
hyper_params["darts"].solver_finetune_test_interval = 50;
hyper_params["darts"].solver_finetune_max_epoch = 400;
hyper_params["darts"].optim_finetune_method = 'sgd';
hyper_params["darts"].optim_finetune_sgd_weight_decay = 0.0001;
hyper_params["darts"].optim_finetune_sgd_momentum = 0.9;
hyper_params["darts"].optim_finetune_sgd_nesterov = false;

/* get the userdatasets */
function get_userdatasets(id, type, datasets, load_predatasets) {
    $.getJSON("index.php?r=cauchy/getdatasets", {id:id, type:type}, function(json) {
        if (json.result == 200) {
            let data = json.data;
            for (var name in data) {
                let dataset = {};
                if (type == 'cls') {
                    dataset.name = name;
                    dataset.records = data[name].dataset_records;
                    dataset.num_classes = data[name].label_info.name_seq.length;
                    dataset.data_dir = userdatasets_root_dir + data[name].dataset_path;
                    dataset.image_tool = "cv2";
                    dataset.input_mode = "BGR";
                    dataset.workers = 4;
                    dataset.keep_difficult = false;
                    dataset.mean_value = [124, 116, 104];

                    /* TODO */
                    dataset.normalize = {};
                    dataset.normalize.div_value = 1;
                    dataset.normalize.mean = [0.485, 0.456, 0.406];
                    dataset.normalize.std = [0.229, 0.224, 0.225];

                    datasets[name] = dataset;

                    details[name] = {};
                    details[name].name_seq = data[name].label_info.name_seq;
                    details[name].color_list = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0],[85, 255, 0], [0, 255, 0], [0, 255, 85], [0, 255, 170], [0, 255, 255],[0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], [170, 0, 255],[255, 0, 255], [255, 0, 170], [255, 0, 85], [255, 0, 170], [255, 0, 85]];

                    train_count = data[name].train_records;
                    test_count = data[name].test_records;
                    train_batchsize = parseInt(0.1 * train_count);
                    test_batchsize = parseInt(0.5 * test_count);
                    console.log(test_count, test_batchsize);
                    dataset_params[name] = {};
                    dataset_params[name].dataset_train_batchsize = train_batchsize;
                    dataset_params[name].dataset_train_sizemode = "fix_size";
                    dataset_params[name].dataset_train_inputsize = 224;
                    dataset_params[name].dataset_train_align_method = "scale_and_pad";
                    dataset_params[name].dataset_val_batchsize = train_batchsize;
                    dataset_params[name].dataset_val_sizemode = "fix_size";
                    dataset_params[name].dataset_val_inputsize = 224;
                    dataset_params[name].dataset_val_align_method = "scale_and_pad";
                    dataset_params[name].dataset_test_batchsize = test_batchsize ;
                    dataset_params[name].dataset_test_sizemode = "fix_size";
                    dataset_params[name].dataset_test_inputsize = 224;
                    dataset_params[name].dataset_test_align_method="scale_and_pad";
                }
            }
        }
        load_predatasets();
    });
}
