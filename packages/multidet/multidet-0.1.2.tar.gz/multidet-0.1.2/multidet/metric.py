import mxnet as mx
from mxnet.gluon import utils as gutils
from time import time

def classify_acc(net, val_iter, ctx=None, max_batch=None, vbn=50):
    """
    在验证集上统计分类模型的top-1测量精度
    后续补充功能：统计各类别的测量精度，以及对应的和总体的top-1、top-5准确率。
    """
    top1_acc = 0
    top5_acc = 0
    num_sample = 0

    if ctx is None:
        ctx = [mx.cpu()]

    print("Evaluate on", ctx)
    start = time()

    batch = 0
    for X, y in val_iter:
        batch += 1
        Xs = gutils.split_and_load(X, ctx_list=ctx, batch_axis=0)
        ys = gutils.split_and_load(y, ctx_list=ctx, batch_axis=0)
        
        y_hats = []
        for data in Xs:
            y_hat = net(data)
            y_hats.append(y_hat)

        for y_hat, label in zip(y_hats, ys):
            top1_acc += (y_hat.argmax(axis=-1) == label.astype(y_hat.dtype)).sum().asscalar()
            top5_acc += ((y_hat.argsort(is_ascend=False)[:,:5] == label.astype(y_hat.dtype).reshape((-1,1))).sum(axis=-1) > 0).sum().asscalar()

            num_sample += len(label)

        if vbn is not None and batch % vbn == 0:
            print("batch %d done"%batch)

        if max_batch is not None and batch >= max_batch:
            break

    print("Use %.2fs"%(time()-start))

    return top1_acc / num_sample, top5_acc / num_sample
