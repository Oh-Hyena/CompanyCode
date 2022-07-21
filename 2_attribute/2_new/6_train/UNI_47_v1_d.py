import tensorflow as tf

#Uni research_47_v1
class Uni_47_v1:
	@staticmethod
	def build(width, height, depth, classes, finalAct="sigmoid"):
		# 인풋 이미지의 차원과, 채널에 해당하는 축을 설정하여 모델을 초기화합니다
		# "channels_last"는 채널의 축이 마지막에 오는 것을 의미합니다
		#model = Sequential()
		x = inputs = tf.keras.Input([height, width, depth])
 
		# input 208,208,3: conv(2,2)
		# conv1 64 (conv(7,7) leaky) 64filter 7*7*2*1 leaky
		# maxpool (2,2) 
		x = tf.keras.layers.Conv2D(64, (7, 7), padding="same",strides=(2, 2), name="conv1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		x = tf.keras.layers.MaxPool2D(pool_size=(2, 2))(x) 
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
		#conv2 64 (conv(1,1) leaky ) 64filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(64, (1, 1), padding="same",strides=(1, 1), name="conv2_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
        
        # conv3 64 (conv(3,3)leaky ) 64filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(64, (3, 3), padding="same",strides=(1, 1), name="conv2_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv4 128 (conv(1,1) leaky) 128filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(128, (1, 1), padding="same",strides=(1, 1), name="conv2_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r1 = x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		#r1 = x = tf.keras.layers.Activation("linear")(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
        
        # residual : -4 concat    
		#x = tf.keras.layers.Concatenate()([x, r1])
        
		# conv5 64 (conv(1,1)leaky ) 64filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(64, (1, 1), padding="same",strides=(1, 1), name="conv3_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		# conv6 64 (conv(3,3)leaky ) 64filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(64, (3, 3), padding="same",strides=(1, 1), name="conv3_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
        
		x = tf.keras.layers.Dropout(0.3)(x)
		# conv7 128 (conv(1,1)linear 128filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(128, (1, 1), padding="same",strides=(1, 1), name="conv3_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.Activation("linear")(x)

        # residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r1])
        
        # conv8 128 (conv(1,1)leaky ) 128filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(128, (1, 1), padding="same",strides=(1, 1), name="conv4_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		# conv9 128 (conv(3,3)leaky ) 128filter 3*3*2*1 leaky
		x = tf.keras.layers.Conv2D(128, (3, 3), padding="same",strides=(2, 2), name="conv4_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		# conv10 256 (conv(1,1)linear ) 256filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv4_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r2 = x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		#r2 = x = tf.keras.layers.Activation("linear")(x)
        
		x = tf.keras.layers.Dropout(0.3)(x)
        # residual : -4 concat    
		#x = tf.keras.layers.Concatenate()([x, r3])
        
		# conv11 128 (conv(1,1)leaky ) 128filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(128, (1, 1), padding="same",strides=(1, 1), name="conv5_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
        
		x = tf.keras.layers.Dropout(0.3)(x)
		# conv12 128 (conv(3,3)leaky ) 128filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(128, (3, 3), padding="same",strides=(1, 1), name="conv5_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		# conv13 256 (conv(1,1)linear ) 256filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv5_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r3 = x = tf.keras.layers.Activation("linear")(x)

        # residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r2])
        
        
		# conv14 128 (conv(1,1)leaky) 128filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(128, (1, 1), padding="same",strides=(1, 1), name="conv6_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		# conv15 128 (conv(3,3)leaky) 128filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(128, (3, 3), padding="same",strides=(1, 1), name="conv6_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)


		# conv16 256 (conv(1,1)linear) 256filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv6_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r4 = x = tf.keras.layers.Activation("linear")(x)
        
		# residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r3])
		
		# conv17 128 (conv(1,1)leaky) 128filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(128, (1, 1), padding="same",strides=(1, 1), name="conv7_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
		# conv18 128 (conv(3,3)leaky) 128filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(128, (3, 3), padding="same",strides=(1, 1), name="conv7_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv19 256 (conv(1,1)linear) 256filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv7_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.Activation("linear")(x)
        
		# residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r4])
        
		# conv20 256 (conv(1,1)leaky) 256filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv8_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
        
		# conv21 256 (conv(3,3)leaky) 256filter 3*3*2*1 leaky
		x = tf.keras.layers.Conv2D(256, (3, 3), padding="same",strides=(2, 2), name="conv8_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		# conv22 512 (conv(1,1)leaky) 512filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(512, (1, 1), padding="same",strides=(1, 1), name="conv8_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r5 = x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		#r4 = x = tf.keras.layers.Activation("linear")(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
   		# residual : -4 concat    
		#x = tf.keras.layers.Concatenate()([x, r3])
        
        # conv23 256 (conv(1,1)leaky) 256filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv9_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv24 256 (conv(3,3)leaky) 256filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (3, 3), padding="same",strides=(1, 1), name="conv9_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		# conv25 512 (conv(1,1)leaky) 512filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(512, (1, 1), padding="same",strides=(1, 1), name="conv9_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r6 = x = tf.keras.layers.Activation("linear")(x)
        
		# residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r5])
 
        # conv26 256 (conv(1,1)leaky) 256filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv10_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv27 256 (conv(3,3)leaky) 256filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (3, 3), padding="same",strides=(1, 1), name="conv10_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
		# conv28 512 (conv(1,1)leaky) 512filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(512, (1, 1), padding="same",strides=(1, 1), name="conv10_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r7 = x = tf.keras.layers.Activation("linear")(x)
        
		# residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r6])

        # conv29 256 (conv(1,1)leaky) 256filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv11_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv30 256 (conv(3,3)leaky) 256filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (3, 3), padding="same",strides=(1, 1), name="conv11_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
		# conv31 512 (conv(1,1)leaky) 512filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(512, (1, 1), padding="same",strides=(1, 1), name="conv11_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r8 = x = tf.keras.layers.Activation("linear")(x)
        
		# residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r7])
		
		# conv32 256 (conv(1,1)leaky) 256filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv12_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv33 256 (conv(3,3)leaky) 256filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (3, 3), padding="same",strides=(1, 1), name="conv12_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
		# conv34 512 (conv(1,1)leaky) 512filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(512, (1, 1), padding="same",strides=(1, 1), name="conv12_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r9 = x = tf.keras.layers.Activation("linear")(x)
        
		# residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r8])
		
		# conv35 256 (conv(1,1)leaky) 256filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (1, 1), padding="same",strides=(1, 1), name="conv13_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv36 256 (conv(3,3)leaky) 256filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(256, (3, 3), padding="same",strides=(1, 1), name="conv13_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
		# conv37 512 (conv(1,1)leaky) 512filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(512, (1, 1), padding="same",strides=(1, 1), name="conv13_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.Activation("linear")(x)
        
		# residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r9])
		
        # conv38 512 (conv(1,1)leaky) 512filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(512, (1, 1), padding="same",strides=(1, 1), name="conv14_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv39		512 (conv(3,3)leaky) 512filter 3*3*2*1 leaky
		x = tf.keras.layers.Conv2D(512, (3, 3), padding="same",strides=(2, 2), name="conv14_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
		# conv40 1024 (conv(1,1)leaky) 1024filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(1024, (1, 1), padding="same",strides=(1, 1), name="conv14_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r10 = x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		#r7 = x = tf.keras.layers.Activation("linear")(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
        
		# residual : -4 concat    
		#x = tf.keras.layers.Concatenate()([x, r8])
	
        # conv41 512 (conv(1,1)leaky) 512filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(512, (1, 1), padding="same",strides=(1, 1), name="conv15_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv42 512 (conv(3,3)leaky) 512filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(512, (3, 3), padding="same",strides=(1, 1), name="conv15_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
		# conv43 1024 (conv(1,1)leaky) 1024filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(1024, (1, 1), padding="same",strides=(1, 1), name="conv15_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		r11 = x = tf.keras.layers.Activation("linear")(x)
        
		# residual : -4 concat    
		x = tf.keras.layers.Concatenate()([x, r10])
     
        # conv44 512 (conv(1,1)leaky) 512filter 1*1*1*1 leaky
		x = tf.keras.layers.Conv2D(512, (1, 1), padding="same",strides=(1, 1), name="conv16_1")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)

		# conv45 512 (conv(3,3)leaky) 512filter 3*3*1*1 leaky
		x = tf.keras.layers.Conv2D(512, (3, 3), padding="same",strides=(1, 1), name="conv16_2")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		
		x = tf.keras.layers.Dropout(0.3)(x)
		
		# conv46 1024 (conv(1,1)leaky) 1024filter 1*1*1*1 linear
		x = tf.keras.layers.Conv2D(1024, (1, 1), padding="same",strides=(1, 1), name="conv16_3")(x)
		x = tf.keras.layers.BatchNormalization()(x)
		#x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
		x = tf.keras.layers.Activation("linear")(x)
        
		# residual : -4 concat    
		x =tf.keras.layers.Concatenate()([x, r11])

        #avgpool
		x = tf.keras.layers.AveragePooling2D(pool_size=7, strides=None, padding='valid')(x)
        
		#FC
		x = tf.keras.layers.Flatten()(x)
 
		# 다중 라벨 분류는 *sigmoid* 활성화 함수를 사용합니다
		x = tf.keras.layers.Dense(classes)(x)
		x = tf.keras.layers.Activation(finalAct)(x)
 
 		# 네트워크 아키텍처를 반환합니다
		return tf.keras.Model(inputs, x )

# IMAGE_DIMS = (224, 224, 3)
# model = Uni_47_v1.build(
	# width=IMAGE_DIMS[1], height=IMAGE_DIMS[0],
	# depth=IMAGE_DIMS[2], classes=24,
	# finalAct="sigmoid")
# model.summary()