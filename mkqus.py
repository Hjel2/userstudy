import os
import subprocess
import random

if __name__ == '__main__':

    total_in_stage_1 = 5
    min_placebo_in_stage_1 = 1
    max_placebo_in_stage_1 = 2

    # increment the count of number of studies conducted
    dir_num = 1
    while os.path.exists(f"{dir_num}"):
        dir_num += 1

    # Stage 1: people's preference is not based on the presence or absence of backdoors
    num_placebos_in_stage_1 = random.randint(min_placebo_in_stage_1, max_placebo_in_stage_1)
    num_backdoored_in_stage_1 = total_in_stage_1 - num_placebos_in_stage_1

    placebos_in_stage_1 = random.sample(list(range(1, 3)), num_placebos_in_stage_1)
    backdoored_in_stage_1 = random.sample(list(range(1, 7)), total_in_stage_1 - num_placebos_in_stage_1)

    order = list(range(1, total_in_stage_1 + 1))
    random.shuffle(order)

    cur_dir = os.path.dirname(__file__)

    subprocess.run(["mkdir", f"{cur_dir}/{dir_num}"])
    subprocess.run(["cp", f"{cur_dir}/template/questions.md", f"{cur_dir}/{dir_num}/questions.md"])
    subprocess.run(["mkdir", f"{cur_dir}/{dir_num}/1"])
    for i in range(num_placebos_in_stage_1):
        subprocess.run(["cp", "-r", f"{cur_dir}/template/placebo/{placebos_in_stage_1[i]}", f"{cur_dir}/{dir_num}/1/{order[i]}"])
    for i in range(total_in_stage_1 - num_placebos_in_stage_1):
        subprocess.run(["cp", "-r", f"{cur_dir}/template/test/{backdoored_in_stage_1[i]}", f"{cur_dir}/{dir_num}/1/{order[i + num_placebos_in_stage_1]}"])

    # Stage 2: people can't find backdoors even when they're looking for them

    backdoored = {
        1: 'test/1/googlenet.py',
        2: 'test/2/mobilenetv2.py',
        3: 'test/3/efficientnetv2.py',
        4: 'test/4/alexnet.py',
        5: 'test/5/swintransformer.py',
        6: 'test/6/convnext.py',
    }

    benign = {
        1: 'test/1/vgg.py',
        2: 'test/2/mnasnet.py',
        3: 'test/3/shufflenetv2.py',
        4: 'test/4/resnet.py',
        5: 'test/5/maxvit.py',
        6: 'test/6/regnet.py',
    }

    placebos = {
        1: (
            'placebo/1/mobilenetv3.py',
            'placebo/1/visiontransformer.py',
        ),
        2: (
            'placebo/2/densenet.py',
            'placebo/2/resnext.py',
        )
    }

    unseen_backdoored = {(i, backdoored[i]) for i in set(range(1, 7)) - set(backdoored_in_stage_1)}
    unseen_placebo = list({benign[i] for i in set(range(1, 7)) - set(backdoored_in_stage_1)} | {placebos[i][0] for i in set(range(1, 3)) - set(placebos_in_stage_1)} | {placebos[i][1] for i in set(range(1, 3)) - set(placebos_in_stage_1)})
    random.shuffle(unseen_placebo)
    unseen_placebo = unseen_placebo[1:]

    order = list(range(1, 6))
    random.shuffle(order)

    subprocess.run(["mkdir", f"{cur_dir}/{dir_num}/2"])

    for i, (x, n) in enumerate(unseen_backdoored): # deal with x == 6!
        subprocess.run(["mkdir", f"{cur_dir}/{dir_num}/2/{order[i]}"])
        subprocess.run(["cp", f"{cur_dir}/template/{n}", f"{cur_dir}/{dir_num}/2/{order[i]}/{n[n.rindex('/') + 1:]}"])

    for i, n in enumerate(unseen_placebo):
        subprocess.run(["mkdir", f"{cur_dir}/{dir_num}/2/{order[i + len(unseen_backdoored)]}"])
        subprocess.run(["cp", f"{cur_dir}/template/{n}", f"{cur_dir}/{dir_num}/2/{order[i + len(unseen_backdoored)]}/{n[n.rindex('/') + 1:]}"])
