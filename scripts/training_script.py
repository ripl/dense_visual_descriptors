import dense_correspondence_manipulation.utils.utils as utils
utils.add_dense_correspondence_to_python_path()
from dense_correspondence.training.training import *
import sys
import time
import logging

#utils.set_default_cuda_visible_devices()
utils.set_cuda_visible_devices([0]) # use this to manually set CUDA_VISIBLE_DEVICES

from dense_correspondence.training.training import DenseCorrespondenceTraining
from dense_correspondence.dataset.spartan_dataset_masked import SpartanDataset
logging.basicConfig(level=logging.INFO)

from dense_correspondence.evaluation.evaluation import DenseCorrespondenceEvaluation

# All of the saved data for this network will be located in the
# code/data_volume/pdc/trained_models/tutorials/caterpillar_3 folder

def pdc_train(dataset_config, train_config, dataset_name, logging_dir, num_iterations, dimension):

    # print("training args")
    # print(dataset_config)
    # print(train_config)
    # print(dataset_name)
    # print(logging_dir)
    # print(num_iterations)
    # print(dimension)
    print('dataset_name')
    print(dataset_name)

    dataset = SpartanDataset(config=dataset_config)

    d = dimension # the descriptor dimension
    name = dataset_name.split('/')[-1] + "_%d" %(d)
    train_config["training"]["logging_dir_name"] = name

    print('logging dir name')
    print(name)

    train_config["training"]["logging_dir"] = logging_dir
    train_config["dense_correspondence_network"]["descriptor_dimension"] = d
    train_config["training"]["num_iterations"] = num_iterations
    print "training descriptor of dimension %d" %(d)
    start_time = time.time()
    train = DenseCorrespondenceTraining(dataset=dataset, config=train_config)
    train.run()
    end_time = time.time()
    print "finished training descriptor of dimension %d using time %.2f seconds" %(d, end_time-start_time)


if __name__ == '__main__':
    dataset_config_file = os.path.join(utils.getDenseCorrespondenceSourceDir(), 'config', 'dense_correspondence', 
                               'dataset', 'composite', 'caterpillar_upright.yaml')
    dataset_config = utils.getDictFromYamlFilename(dataset_config_file)
    dataset_config['logs_root_path'] = 'logs_proto_default_scaling_gt_pose'

    train_config_file = os.path.join(utils.getDenseCorrespondenceSourceDir(), 'config', 'dense_correspondence', 
                                'training', 'training.yaml')
    train_config = utils.getDictFromYamlFilename(train_config_file)
    
    dataset_name = "logs_proto_default_scaling_gt_pose"
    logging_dir = "trained_models/new_test_caterpillar/"
    num_iterations = (1500/4)-1
    dimension = 3

    pdc_train(dataset_config, train_config, dataset_name[11:], logging_dir, num_iterations, dimension)