
	//--------------Simple Direction Selective Network--------------//
	//--------------One DSGC with voltage gated channels
	//--------------Excitatory input from Bipolar cells and SACs
	//--------------Inhibitory input from SACs
	//--------------Presynaptic cells not explicitly modelled
	//--------------Realistic synaptic conductances
	//
	//			SAC				Bipolar
	//			|	|				|
	//		GABA	ACH			AMPA/NMDA
	//		____________DSGC____________
	//
	//		2015 Alon Poleg-Polsky
	//		polegpolskya@mail.nih.gov
	//---------------------------------------------------------------//

	if (unix_mac_pc()==1){
		nrn_load_dll("./x86_64/.libs/libnrnmech.so")
		load_file("./RGCmodel3.hoc")
	}else{
		load_file("nrngui.hoc")
		load_file("RGCmodel3.hoc")
		startseed=1
	}

	//--------------MAIN SIMULATION PARAMETERS

	filesavenum=startseed							//where to save
	exptype=2								//Recording type
											//1:AP
											//2:PSP
											//3:EPSC
											//4:IPSC

	use_active=0							//1-active conductances; 0- only passive
	tstop=600								//simulation run time >>1200
	maxvesmul=1
	//conx=5
	//numdendskip=10
	//--------------SYNAPTIC CONDUCTANCES
	sparse=1//8						 		//sparse distribution of bipolar inputs control>>1 sparse 1/3
	b2gampa=(0.25)/sparse/maxvesmul			//bipolar to DSGC AMPA conductance (nS) >>0.1
	b2gnmda=.5/sparse/maxvesmul 			//bipolar to DSGC conductance (nS)	>>0.2
	s2ggaba=.5/maxvesmul 					//SAC to DSGC inhibitory conductance (nS)	>>0.2
	s2gach=.5/maxvesmul					//SAC to DSGC excitatory conductance (nS)	>>0.2
	gabaMOD=.33*1 //*3						//SAC inhibitory release voltage relative to Bipolar votage (used to generate DS in SAC input	pref>>0.33 null>>1
	achMOD=0.25*1 //*4						//same for excitatory drive from SAC

	//--------------MORE PARAMETERS
	dt=0.1									//integration time
	INHIBnum=2								//number of inhibitory levels
	REPEATnum=3								//number of repeats
	GROUPnum=2//80							//number of repeats
	seed2=startseed							//random generator, any number
	BIPVamp=1			      				//amplitude of the light evoked bipolar depolarization (AU)>>1
	BIPVbase=0	     						//bipolar rest (AU)		>>0
	SACVamp=BIPVamp				   			//amplitude of the light evoked SAC depolarization (AU)
	SACVbase=BIPVbase      					//SAC rest (AU)
	maxves_bipNMDA=10*maxvesmul				//RRP from each presynaptic synapse
	maxves_SACinhib=maxves_bipNMDA
	maxves_SACexc=maxves_bipNMDA
	//-------------------VISUAL INPUT
	lightstart=-100     						//start time of the stimulus bar(ms) >>300
	lightspeed=1		       				//speed of the stimulus bar (um/ms)	>>1
	lightwidth=500			     			//width of the stimulus bar(um)			>>1000
	lightXstart=-100       					//start location (X axis)of the stimulus bar (um) 	>>-100
	lightXend=200        					//end location (X axis)of the stimulus bar (um)		>>200
	lightYstart=-130       					//start location (Y axis) of the stimulus bar (um)	>>-130
	lightYend=100        					//end location (Y axis) of the stimulus bar (um)	>>100
	lightreverse=0							//direction	of light sweep (left>right;right<left)	>>0
	// if (gabaMOD<1){SACdelt=50
	// }else{SACdelt=-50}					//delay between SAC and Bipolar light mediated inputs(ms)>>0
	SACdelt=0
	SACdelx=0								//offset of the SAC receptive field (um)			>>0
	SACdur=500								//Additional duration of SAC depolarization following the stimulus>>500
	inhibamp=1
	//------------------SYNAPTIC/VGC PARAMS
	VampK_bipNMDA=5
	VampK_SACinhib=VampK_bipNMDA
	VampK_SACexc=VampK_bipNMDA
	VampT=1
	Transient=250//ms
	n_bipNMDA=0.3 							//Params of voltage dependent NMDA activation 	>>0.2
	gama_bipNMDA=0.07 						//Params of voltage dependent NMDA activation 	>>0.08
	newves_bipNMDA=0.002					//Rate of addition of new Vesicles to the RRP	>>0.002
	newves_SACinhib=0.003					//Rate of addition of new Vesicles to the RRP	>>0.003
	// Vtau1_bipNMDA=20//50						//Risetime for Bipolar Vm after stimulus input (ms)		>>50
	// Vtau2_bipNMDA=200//200						//Decaytime for Bipolar Vm after stimulus input (ms)	>>200
	tau1NMDA_bipNMDA=60//100						//Decaytime for NMDA activation (ms)			>>50
	//tau1NMDA_bipNMDA=3
	//tau2NMDA_bipNMDA=1
	// Vtau1_SACinhib=20//50						//Risetime for SAC Vm after stimulus input (ms)	>>50
	// Vtau2_SACinhib=500//200						//Decaytime for SAC Vm after stimulus input (ms)>>200
	// Vtau1_SACexc=20//50							//Risetime for SAC Vm after stimulus input (ms)	>>50
	// Vtau2_SACexc=200//200						//Decaytime for SAC Vm after stimulus input (ms)>>200
	newves_SACexc=newves_bipNMDA					//Rate of addition of new Vesicles to the RRP	>>0.002
	tau_SACexc=3							//Decaytime for ACH activation (ms)				>>3
	e_SACinhib=-60//-60//5					//SAC mediated inhibitory reversal potential (mV)>>-65
	tau_SACinhib=30							//Tau decay of GABA inhibition (ms)				>>30
	vshift_HHst=-5						//DSGC voltage gated channel Vm change (fine tuning)>>-3, positive-more AP
	// BIPnoise=0.1							//Variablity of bipolar release voltage 1	>>0.2
	// SACnoise=0.2							//Variablity of SAC release voltage 1		>>0.2
	// Vnoiseamp_bipNMDA=0.2					//Variablity of bipolar release voltage 2	>>0.2
	// Vnoiseamp_SACinhib=0.2					//Variablity of SAC release voltage 2		>>0.2
	// Vnoiseamp_SACexc=0.2					//Variablity of SAC release voltage 2		>>0.2
	// Vnoiserate_SACinhib=10					//Variablity of SAC release voltage 2		>>10
	// Vnoiserate_SACexc=10					//Variablity of SAC release voltage 2		>>10
	rSYNchance=1//.5							//chance to have a bipolar/SAC input per each DSGC dend		>>0.7
	NMDAspike_dur=30
	NMDAspike_V=-40
	NF_HHst=0
	// Vnoise_bipNMDA=0						//visual noise	>>0
	// Vnoise_SACinhib=Vnoise_bipNMDA
	// Vnoise_SACexc=Vnoise_bipNMDA
	noisecounter=0
	Voff_bipNMDA=0//*
	Vset_bipNMDA=-48//*
	flickertime=50
	flickerVAR=0//13//.1//0.03
	stimnoiseVAR=0//10//01//10
	//NFleak_HHst=0
	//tau1NMDA_bipNMDA=3//*
	//tau2NMDA_bipNMDA=0.1//*

	//---------------OBJECTS
	objref RGC,rtime ,rnoise,RGCsomaAP,netcon,rbackground,temp,filesave,nil,pc,rBIP	,tempAP
	objref RecV[2][2][2],AMPA[2][2][2],NMDA[2][2][2],ACH[2][2][2],GABA[2][2][2],recDEND[2],recDENDtemp
	double gatherdata[2][2][2],gatherdataN[2][2][2],gatherdataI[2][2][2]
	objref fileAMPA,fileNMDA,fileACH,fileGABA,VOLClamp,fileDEND	,rundendV[2]
	objref Vvec,AMPAvec,NMDAvec,ACHvec,GABAvec
	Vvec=new Vector()
	AMPAvec=new Vector()
	NMDAvec=new Vector()
	ACHvec=new Vector()
	GABAvec=new Vector()
	rtime=new Random()
	rtime.ACG(seed2)
	rnoise=new Random()
	rnoise.ACG(seed2)
	rbackground=new Random()
	rBIP=new Random()
	rBIP.ACG(seed2)
	pc = new ParallelContext()



	proc  init_active(){
		//***initialization of active voltages parameters
		doingVC=0
		if (exptype>=3){
			doingVC=1
		}
		TTX=0
		if (exptype==2){
			TTX=1
		}
		VOLClamp=new OClamp(0.5)
		VOLClamp.on=0
		VOLClamp.off=100000
		VOLClamp.rs=20
		VOLClamp.switched_on=doingVC
		VOLClamp.vc=-60
		if (exptype==4){
			VOLClamp.vc=0
		}

		active=1-doingVC

		//SOMA
		RGCsomana=00.35*active*(1-TTX)						//.3
		RGCsomakv=0.07*active						//.07//.004
		RGCsomakm=00.003*active//0.00005*active
		//DEND
		RGCdendna=0.0002*(1-TTX)
		RGCdendkv=0.007*active	//.002
		RGCdendkm=0*active
		RGCcaT=0*active
		RGCcaL=0.0*active
		RGCcaP=0*active
		RGCih=0*active
		RGCkca=0*active
		RGCgpas=2e-5*(1+active*10)
		RGCepas	=-60
	}
	objref tempV

	proc par_run(){
		//the actual function executed on multiple cores (parallel processing)
		objref RGCsomaAP,netcon,nil
		RGCsomaAP=new Vector()
		netcon=new NetCon(&RGC.soma.v(0.5),nil)         //AP count
		netcon.record(RGCsomaAP)
		netcon.threshold=-10
		objref rundendV[RGC.numsyn]
		i=0
		forsec RGC.ON{	//on On-dendrites
			rundendV[i]=new Vector()
			rundendV[i].record(&v(0.5))
			i=i+1
		}
		Vvec.record(&RGC.soma.v(0.5))

		recDENDtemp=new Vector(RGC.countON*tstop/dt+1)//recording of dendritic signals
		strdef outstr
		sec=seed2
		if (unix_mac_pc()==1){
			system("date +%N",outstr)
			sscanf(outstr,"%i",&sec)
		}
		seed2=sec+1
		//placeBIP()
		init_active()
		if (doingVC==1){
			Vvec.record(&VOLClamp.i)
		}
		global_ra = 100
		Ra=global_ra
		celsius = 36.9
		gabaMOD=0.25+.75*$1
		//gabaMOD=0.33+.67*$1
		//achMOD=.001*$1//.25*$3+.8

		b2gampa=$3*.001//$3/10*2
				//BIPVamp=$3
				//SACVamp=BIPVamp
				//SACVbase=BIPVbase

		update()
		placeBIP()
		forall{finitialize(-60)}
					//save vectors (voltages/conductances)
		AMPAvec=new Vector(tstop/dt+2)
		NMDAvec=new Vector(tstop/dt+2)
		ACHvec=new Vector(tstop/dt+2)
		GABAvec=new Vector(tstop/dt+2)
		t=0
		while (t < tstop) {
            fadvance()
			for i=0,RGC.numsyn-1{
				AMPAvec.x[t/dt]=AMPAvec.x[t/dt]+RGC.BIPsyn[i].gAMPA
				NMDAvec.x[t/dt]=NMDAvec.x[t/dt]+RGC.BIPsyn[i].gNMDA
				ACHvec.x[t/dt]=ACHvec.x[t/dt]+RGC.SACexcsyn[i].g
				GABAvec.x[t/dt]=GABAvec.x[t/dt]+RGC.SACinhibsyn[i].g
			}
			count=0
			forsec	RGC.ON{
				recDENDtemp.x[count*tstop/dt+t/dt]=v(0.5)
				count=count+1
			}
		}
		//counts NMDA spikes based on amplitude and duration
		NMDAspike_count=0
		count=0
		forsec RGC.ON{
			length=0
			found=0
			if (RGC.BIPsyn[count].Vdel<100000){
				for t=0,tstop-1{
					if (rundendV[count].x[t/dt]>=NMDAspike_V){
						length=length+1
						if (length>=NMDAspike_dur){
							found=found+1
							length=0
						}
					}else{
						length=0
					}
				}
				NMDAspike_count=NMDAspike_count+found
			}
			count=count+1
		}
		result=RGCsomaAP.size()
		print $1,$2,$3,$4
		for i=0,RGCsomaAP.size()-1{print RGCsomaAP.x[i]}
		if (exptype>=2)		{
			//result=Vvec.mean(lightstart/dt+200/dt,lightstart/dt+500/dt)-Vvec.mean(100/dt,lightstart/dt)
			result=Vvec.max()+60
			//result=Vvec.max()+60
		}
		countN=0//number of active synapses
		for i=0,RGC.numsyn-1{
			if (RGC.BIPsyn[i].Vdel<100000){
				countN=countN+1
			}
		}
		pc.post("done", $1,$2,$3,$4,result,NMDAspike_count,countN,Vvec,AMPAvec,NMDAvec,ACHvec,GABAvec,recDENDtemp)
	}

	proc brun(){
		//the master function to trigger execution on multiple cores
		objref Vvec
		Vvec=new Vector()
		init_active()
		SACVamp=BIPVamp				   			//amplitude of the light evoked SAC depolarization (AU)
		SACVbase=BIPVbase
		update()
		double gatherdata[INHIBnum][REPEATnum][GROUPnum],gatherdataI[INHIBnum][REPEATnum][GROUPnum],gatherdataN[INHIBnum][REPEATnum][GROUPnum]
		pc.runworker()
		objref RecV[INHIBnum][REPEATnum][GROUPnum],AMPA[INHIBnum][REPEATnum][GROUPnum],NMDA[INHIBnum][REPEATnum][GROUPnum],ACH[INHIBnum][REPEATnum][GROUPnum],GABA[INHIBnum][REPEATnum][GROUPnum]
		objref recDENDtemp,recDEND[RGC.countON]
		recDENDtemp=new Vector(2)
		index=0
 		for INHIBcount=0,INHIBnum-1{
			for REPEATcount=0,REPEATnum-1{
				for GROUPcount=0,GROUPnum-1{
					RecV[INHIBcount][REPEATcount][GROUPcount]=new Vector()
					AMPA[INHIBcount][REPEATcount][GROUPcount]=new Vector()
					NMDA[INHIBcount][REPEATcount][GROUPcount]=new Vector()
					ACH[INHIBcount][REPEATcount][GROUPcount]=new Vector()
					GABA[INHIBcount][REPEATcount][GROUPcount]=new Vector()
					pc.submit(index,"par_run",INHIBcount,REPEATcount,GROUPcount,index)
					index=index+1
				}
			}
		}
		while (pc.working()) {
			result=0
			resultI=0
			resultN=0
			pc.take("done", &INHIBcount,&REPEATcount,&GROUPcount,&index,&result,&resultI,&resultN,Vvec,AMPAvec,NMDAvec,ACHvec,GABAvec,recDENDtemp)
			gatherdata[INHIBcount][REPEATcount][GROUPcount]=result
			gatherdataI[INHIBcount][REPEATcount][GROUPcount]=resultI
			gatherdataN[INHIBcount][REPEATcount][GROUPcount]=resultN
			RecV[INHIBcount][REPEATcount][GROUPcount].copy(Vvec)
			AMPA[INHIBcount][REPEATcount][GROUPcount].copy(AMPAvec)
			NMDA[INHIBcount][REPEATcount][GROUPcount].copy(NMDAvec)
			ACH[INHIBcount][REPEATcount][GROUPcount].copy(ACHvec)
			GABA[INHIBcount][REPEATcount][GROUPcount].copy(GABAvec)
			for count=0,RGC.countON-1{
				recDEND[count]=new Vector(tstop/dt)
				for time=0,tstop/dt-1{
					recDEND[count].x[time]=recDENDtemp.x(count*tstop/dt+time)
				}
			}
		}
		pc.done()
		//---------------saving to files
		strdef st,basest,stAMPA,stNMDA,stACH,stGABA
		fileDEND=new File()
		filesave=new File()
		fileAMPA=new File()
		fileNMDA=new File()
		fileACH=new File()
		fileGABA=new File()
		//---------------actual voltages
		if (unix_mac_pc()==1){
			sprint(basest,"./OUTPUT/SIM_%d",filesavenum)
		}else{
			sprint(basest,"OUTPUT/SIM_%d",filesavenum)
		}
		sprint(st,"%s_DEND.dat",basest)
		fileDEND.wopen(st)
		sprint(st,"%s_Vm.dat",basest)
		filesave.wopen(st)
		sprint(st,"%s_AMPA.dat",basest)
		fileAMPA.wopen(st)
		sprint(st,"%s_NMDA.dat",basest)
		fileNMDA.wopen(st)
		sprint(st,"%s_ACH.dat",basest)
		fileACH.wopen(st)
		sprint(st,"%s_GABA.dat",basest)
		fileGABA.wopen(st)
		for INHIBcount=0,INHIBnum-1{
			for GROUPcount=0,GROUPnum-1{
				for REPEATcount=1,REPEATnum-1{
					RecV[INHIBcount][0][GROUPcount].add(RecV[INHIBcount][REPEATcount][GROUPcount])
				}
				RecV[INHIBcount][0][GROUPcount].div(REPEATnum)
			}
		}

		for time=0,RecV[0][0][0].size()-1{
			st=""
			stAMPA=""
			stNMDA=""
			stACH=""
			stGABA=""

			for INHIBcount=0,INHIBnum-1{
				for REPEATcount=0,REPEATnum-1{
					for GROUPcount=0,GROUPnum-1{
						if (INHIBcount+GROUPcount>0){
							sprint(st,"%s	",st)
							sprint(stAMPA,"%s	",stAMPA)
							sprint(stNMDA,"%s	",stNMDA)
							sprint(stACH,"%s	",stACH)
							sprint(stGABA,"%s	",stGABA)
						}
						sprint(st,"%s%g",st,RecV[INHIBcount][REPEATcount][GROUPcount].x[time])
						sprint(stAMPA,"%s%g",stAMPA,AMPA[INHIBcount][REPEATcount][GROUPcount].x[time])
						sprint(stNMDA,"%s%g",stNMDA,NMDA[INHIBcount][REPEATcount][GROUPcount].x[time])
						sprint(stACH,"%s%g",stACH,ACH[INHIBcount][REPEATcount][GROUPcount].x[time])
						sprint(stGABA,"%s%g",stGABA,GABA[INHIBcount][REPEATcount][GROUPcount].x[time])
					}
				}

			}
			sprint(st,"%s\n",st)
			sprint(stAMPA,"%s\n",stAMPA)
			sprint(stNMDA,"%s\n",stNMDA)
			sprint(stACH,"%s\n",stACH)
			sprint(stGABA,"%s\n",stGABA)
			filesave.printf(st)
			fileAMPA.printf(stAMPA)
			fileNMDA.printf(stNMDA)
			fileACH.printf(stACH)
			fileGABA.printf(stGABA)
		}

		for time=0,recDEND[0].size()-1{
			sprint(st,"%g",recDEND[0].x[time])
			for count=1,RGC.countON-1{
				sprint(st,"%s	%g",st,recDEND[count].x[time])
			}
			sprint(st,"%s\n",st)
			//fileDEND.printf(st)
		}

		fileDEND.close()
		filesave.close()
		fileAMPA.close()
		fileNMDA.close()
		fileACH.close()
		fileGABA.close()

		if (unix_mac_pc()==1){
			sprint(st,"./OUTPUT/SIM_%d.dat",filesavenum)
		}else{
			sprint(st,"OUTPUT/SIM_%d.dat",filesavenum)
		}
		filesave.wopen(st)
		for REPEATcount=0,REPEATnum-1{
			for GROUPcount=0,GROUPnum-1{
				st=""
				for INHIBcount=0,INHIBnum-1{
					sprint(st,"%s%g	",st,gatherdata[INHIBcount][REPEATcount][GROUPcount])
				}
				sprint(st,"%s\n",st)
				filesave.printf(st)
			}
		}
		filesave.close()

	}

	objref noisevecBIP[2],noisevecSACI[2],noisevecSACE[2],basenoise	,ampnoise	,mulnoise	,g

	func minval(){
		if (($1<0)||($2<0)){return 0}
		if ($1<$2){
			return $1
		}else{
			return $2
		}
	}
	func convertlight(){
		//***Conversion of  light into linear units
		if ($1<=0){
			calcreturn=0
		}else{
			//calcreturn=-.00123+1/(1+exp(-($1-7.3348)/1.54))		//-.00123+.72171/(1+exp(-($1-7.3348)/1.54))
			//calcreturn=.007+.9/(1+exp(-($1-8)/.5))
			//calcreturn=.008/(1+exp(-($1-.004)/.0015))
			calcreturn=$1//.01/(1+exp(-($1-.004)/.001))
		}
		return calcreturn
	}
	proc placeBIP(){
		//***Placement of Bip and SAC inputs on the dendrties of the DSGC
		count=0
		rBIP.ACG(seed2)
		rBIP.uniform(0,1)
		rnoise.ACG(seed2)
	    rnoise.normal(0,flickerVAR)

		objref noisevecBIP[RGC.numsyn],noisevecSACI[RGC.numsyn],noisevecSACE[RGC.numsyn],basenoise,ampnoise,mulnoise
		basenoise=new Vector(tstop/dt+1,0)
		ampnoise=new Vector(tstop/dt+1,0)
		mulnoise=new Vector(tstop/dt+1,0)
		for timer=0,tstop/flickertime-1{
			basenoise.fill((BIPVbase+rnoise.normal(0,flickerVAR)),timer*flickertime/dt,(timer+1)*flickertime/dt)
			ampnoise.fill((BIPVamp+rnoise.normal(0,flickerVAR+stimnoiseVAR)),timer*flickertime/dt,(timer+1)*flickertime/dt)
		}
		for i=0,basenoise.size()-1{
			basenoise.x[i]=convertlight(basenoise.x[i])
			ampnoise.x[i]=convertlight(ampnoise.x[i])

		}


		for synnum=0,RGC.numsyn-1{
			//---------------BIP
			noisevecBIP[synnum]=new Vector(tstop/dt+1,0)
			noisevecSACI[synnum]=new Vector(tstop/dt+1,0)
			noisevecSACE[synnum]=new Vector(tstop/dt+1,0)
			starttime=tstop
			if (rBIP.repick<rSYNchance*sparse){//found close dend
				count=count+1
				if (lightspeed==0){	//stationary light input
					starttime=lightstart//rtime.normal(lightstart,lightstartvariance)
				}else{  			//moving bar
	               	if (lightreverse){
    	              	starttime=(lightstart+(lightXend-RGC.BIPsyn[synnum].locx)/lightspeed)
        	       	}else{
            	    	starttime=(lightstart+(RGC.BIPsyn[synnum].locx-lightXstart)/lightspeed)
               		}
               	}
				noisevecBIP[synnum].copy(basenoise)
				noisevecBIP[synnum].copy(ampnoise,minval(starttime/dt,tstop/dt),minval(starttime/dt,tstop/dt),minval((starttime+lightwidth)/dt,tstop/dt))

				mulnoise.fill(1)
				mulnoise.fill(VampT,minval(starttime/dt,tstop/dt),minval((starttime+Transient)/dt,tstop/dt))
				noisevecBIP[synnum].mul(mulnoise)
				for i=0,noisevecBIP[synnum].size()-1{
					//noisevecBIP[synnum].x[i]=convertlight(noisevecBIP[synnum].x[i])
				}
			}
			noisevecBIP[synnum].play(&RGC.BIPsyn[synnum].Vinf,dt)
			//------------SACinhibsyn
			if (rBIP.repick<rSYNchance){//found close dend
				if (lightspeed==0){	//stationary light input
					starttime=lightstart//rtime.normal(lightstart,lightstartvariance)+SACdelt
				}else{  			//moving bar
	               	if (lightreverse){
    	              	starttime=(lightstart+(lightXend-RGC.SACinhibsyn[synnum].locx)/lightspeed)+SACdelt
        	       	}else{
            	    	starttime=(lightstart+(RGC.SACinhibsyn[synnum].locx-lightXstart)/lightspeed)+SACdelt
               		}
               	}
				noisevecSACI[synnum].copy(basenoise)
				noisevecSACI[synnum].copy(ampnoise,minval(starttime/dt,tstop/dt),minval(starttime/dt,tstop/dt),minval((starttime+lightwidth)/dt,tstop/dt))
				mulnoise.fill(1)//gabaMOD
				mulnoise.fill(VampT*gabaMOD,minval(starttime/dt,tstop/dt),minval((starttime+Transient+SACdur)/dt,tstop/dt))
				noisevecSACI[synnum].mul(mulnoise)
				for i=0,noisevecSACI[synnum].size()-1{
					//noisevecSACI[synnum].x[i]=convertlight(noisevecSACI[synnum].x[i])
				}
			}
			noisevecSACI[synnum].play(&RGC.SACinhibsyn[synnum].Vinf,dt)
			//--------------SACexcsyn
			if (rBIP.repick<rSYNchance){//found close dend
				if (lightspeed==0){	//stationary light input
					starttime=lightstart//rtime.normal(lightstart,lightstartvariance)+SACdelt
				}else{  			//moving bar
	               	if (lightreverse){
    	              	starttime=(lightstart+(lightXend-RGC.SACinhibsyn[synnum].locx)/lightspeed)+SACdelt
        	       	}else{
            	    	starttime=(lightstart+(RGC.SACinhibsyn[synnum].locx-lightXstart)/lightspeed)+SACdelt
               		}
               	}
				noisevecSACE[synnum].copy(basenoise)
				noisevecSACE[synnum].copy(ampnoise,minval(starttime/dt,tstop/dt),minval(starttime/dt,tstop/dt),minval((starttime+lightwidth)/dt,tstop/dt))
				mulnoise.fill(1)
				mulnoise.fill(VampT*achMOD,minval(starttime/dt,tstop/dt),minval((starttime+Transient+SACdur)/dt,tstop/dt))
				noisevecSACE[synnum].mul(mulnoise)
				for i=0,noisevecSACE[synnum].size()-1{
					//noisevecSACI[synnum].x[i]=convertlight(noisevecSACE[synnum].x[i])
				}
			}
			noisevecSACE[synnum].play(&RGC.SACexcsyn[synnum].Vinf,dt)

		}
	}

	proc update(){
		//***Update of variables in the simulation
		//-----SYNAPSES
		seed_HHst=seed2
		gAMPAsingle_bipNMDA=b2gampa
		gNMDAsingle_bipNMDA=b2gnmda
		gsingle_SACinhib=s2ggaba
		gsingle_SACexc=s2gach
		//-----RGC
		if(use_active){
			access RGC.soma
			distance()
			forsec RGC.somas{
				gnabar_HHst= RGCsomana
				gkbar_HHst= RGCsomakv
				gkmbar_HHst= RGCsomakm
			}
			forsec RGC.all{
				glbar_HHst=RGCcaL
				gtbar_HHst=RGCcaT
				gleak_HHst=RGCgpas/2
				eleak_HHst=RGCepas
			}
			forsec RGC.dends{
				gnabar_HHst= RGCdendna
				gkbar_HHst= RGCdendkv
				gkmbar_HHst=RGCdendkm
			}
		}else{
			forsec RGC.all{
				g_pas=RGCgpas
				e_pas=RGCepas
			}
		}
 	}//UPDATE

	proc init_sim(){
		//***STARTS THE SIMULATION-----//
		RGC=new DSGC(0,0)
		placeBIP()
		forall{
			if(use_active){
				insert HHst
			}else{
				insert pas
			}
			global_ra = 100
			Ra=global_ra
		}
		count=0
		forsec RGC.ON{
			count=count+1
		}
	}


	//---------------INITIALIZATION

	init_sim()
	init_active()
	update()
	//placeBIP()
	access RGC.soma


	update()
   	if (unix_mac_pc()==1){
		brun()
    	quit()
    }else{
		load_file("model.ses")
		//brun()
	}
