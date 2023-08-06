from keras.callbacks import Callback
from keras import backend as K

class inn_callback(Callback):
    tid=""
    conn=None
    def set_cb_params(self,tid,conn,step,epoch_shift,target_net,results_folder,eval_values,loss_values,es_values,val_input,val_output,evaluator,stopper,target_update_lr,target_lra_args):
        self.tid=tid
        self.conn=conn
        self.step=step
        self.epoch_shift=epoch_shift
        self.target_net=target_net
        self.results_folder=results_folder
        self.eval_values=eval_values
        self.loss_values=loss_values
        self.es_values=es_values
        self.val_input=val_input
        self.val_output=val_output
        self.evaluator=evaluator
        self.stopper=stopper
        self.target_update_lr=target_update_lr
        self.target_lra_args=target_lra_args

    def get_loss(self):
        return self.loss

    def checkpoint(self):
        savname="%s/%s_checkpoint_%d.wei"%(self.results_folder,self.tid,self.real_epoch)
        #print("checkpoing with savname=%s"%(savname))
        self.model.save(savname)
        self.conn.root.set_checkpoint(self.tid,str(self.real_epoch),savname)
        completion=100*float(self.real_epoch)/float(self.params["epochs"])
        #print("completion=%f"%(completion))
        self.conn.root.set_completion(self.tid,completion)

    def on_epoch_end(self,epoch,logs):
        #print("tid=%s epoch %d/%d"%(self.tid,epoch,self.params["epochs"]))
        self.real_epoch=epoch+self.epoch_shift
        self.loss=logs["loss"]
        #print("real_epoch=%d step=%d"%(self.real_epoch,self.step))
        if self.step!=None and self.real_epoch%self.step==0:
            self.checkpoint()
        
        #set last epoch
        self.es_values[0]=self.real_epoch

        #get loss function
        self.loss_values.append(self.get_loss())

        #evaluate 
        if self.evaluator!=None:
            eval_v=self.evaluator(self.target_net,self,self.val_input,self.val_output)
            #print("eval=%s"%(eval_v))
            self.eval_values.append(eval_v)

            #early stopping
            if self.stopper!=None: 
                if self.stopper.testing(eval_v):
                    print("early stopping at epoch %d"%(self.real_epoch))
                    self.model.stop_training=True

        #update the leaning rate 
        if self.target_update_lr!=None:
            lr=K.get_value(self.model.optimizer.lr)
            new_lr=self.target_update_lr(lr,self.target_lra_args,self.params["epochs"])
            K.set_value(self.model.optimizer.lr,new_lr)
