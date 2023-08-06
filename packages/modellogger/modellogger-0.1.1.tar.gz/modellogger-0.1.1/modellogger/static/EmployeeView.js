///////////////////////////////////////////////Define Movie store ///////////////////////////////////////////////
Ext.define('Movies', {
    extend: 'Ext.data.Model',
    fields: [{
        name: 'id',
    },{
        name: 'UserId',
    }, {
        name: 'ScannedFiles'
    },{
    name: 'RiskFiles',
    },{
    name: 'ScanStatus',
    },{
    name: 'Time',
    },{
    name: 'Date',
    },{
    name: 'Filename',
    },{
    name: 'IsValid',
    }]

}

);



Ext.onReady(function() {
    //var data = [];
       console.log('on ready done');

    var store = Ext.create('Ext.data.Store', {
        model: 'Movies',
         
    		proxy : {
        
            
    
    		type : 'ajax',
    		actionMethods : {
    		read : 'POST'
    		},
    		// action class movie_action mapped to InputServlet
    		url : 'InputServlet',
    		extraParams: {
    		},
    		reader : {
    		type : 'json',
    		// json value for list
    		rootProperty : 'movie_list',
    		keepRawData :true
    		}
    		},

    		autoLoad : true
    });
    
Ext.define('deleteAll', {
    extend: 'Ext.data.Model',
    fields: ['value'],

    proxy: {
        type: 'rest',
        url : '/scan'
    }
    // autoLoad : true
});













    var grid = Ext.create('Ext.grid.Panel', {
    	width: "100%",
    	height: 500,
    	title: 'Simple',
    	store: store,
    	header: false,
    	columns: [{
            //anything
            text: 'SlNo.',
            //json key name
            dataIndex: 'id',
            width: 140
        },{
    		//anything
    		text: 'UserId',
    		//json key name
    		dataIndex: 'UserId',
    		width: 140
    	},
    	
    	{
    		text: 'ScannedFiles',
    		dataIndex: 'ScannedFiles',
    		width: 200
    	},

    	{
    		text: 'RiskFiles',
    		dataIndex: 'RiskFiles',
    		width: 200
    	},
    	
    	{
    		text: 'ScanStatus',
    		dataIndex: 'ScanStatus',
    		width: 180
    	},
    	
    	{
    		text: 'Time',
    		dataIndex: 'Time',
    		width: 160
    	},
    	{
    		text: 'Date',
    		dataIndex: 'Date',
    		width: 200
    	},
        {
            text: 'Filename',
            dataIndex: 'Filename',
            width: 200
        },
        {
            text: 'IsValid',
            dataIndex: 'IsValid',
            width: 200
        }],
    });
    
    var textfeilds={ 
    		//xtype: 'textfield',
    		width:"100%",
    		layout: 'hbox',
    	    items:
    	        [
    	     
    		 {
             	fieldLabel: 'File Name',
                 name: 'Filename',
                 xtype: 'textfield',
                 margin: '10px 10px 10px 163px',
                 placeholder: 'Enter the file name',
                 allowBlank : false
             },
             {
              
                 fieldLabel: 'Date of scan',
                 name: 'Date',
                 xtype: 'datefield',
                 format: 'Y-m-d',
                 margin: '10px 10px 10px 163px',
                 placeholder: 'Enter the date of scan',
                 allowBlank : false
             },
   ] };
    
    
    var comboxes ={ 
         //   xtype: 'combo',
            layout: 'hbox',
            width:"100%",
    		items: 
    	
    	[
        
        {

            fieldLabel: 'Scan Status',
            name: 'ScanStatus',
            allowBlank : false,
            xtype: 'combo',
            margin: '10px 10px 10px 163px',
            placeholder: 'Enter Scan Status',
            store: new Ext.data.SimpleStore({
        		data: [
        			[1, 'completed'],
        			[2, 'error'],
        			
        		],
        		id: 0,
        		fields: ['value', 'text']
        	}),
        },
        {
//////////////////  creating external stores for combo box ///////////////
            fieldLabel: 'Valid Flag',
            name: 'IsValid',
            xtype: 'combo',
            allowBlank : false,
            margin: '10px 10px 10px 163px',
            placeholder: 'Enter Valid Flag',
            store: new Ext.data.SimpleStore({
        		data: [
        			[1, 0],
        			[2, 1],
        		],
        		id: 0,
        		fields: ['value', 'text']
        	}),
        },
    ]};






    var textfeilds2={ 
            //xtype: 'textfield',
            width:"100%",
            layout: 'hbox',
            items:
                [
             
             {
              
                 fieldLabel: 'Scan Directory',
                 name: 'path',
                 xtype: 'textfield',
                 margin: '10px 10px 10px 50px',
                 placeholder: 'Enter the path for scan field',
                 allowBlank : false
             },
   ] };




    var buttons={
    		 items: [
    		  {
///////////////////////search button calling the proxy //////////////////////////    			  
    		    	xtype:'button',
    		    	text:"Search",
    		        margin: '10px 10px 10px 163px',
    		        handler: function(){
    		            var form = this.up('form').getForm(); 
    		            store.getProxy().extraParams=form.getValues();
    		            this.up('form').getForm().reset();
    		            store.reload();
                        console.log('search');
    		        }
    		        
    		    },
    		    {
////////////////////////reset button //////////////////////////////////////////    		    	
    		    	xtype:'button',
    		    	text:"reset",
    		        margin: '10px 10px 10px 180px',
    		        handler: function(){
    		        	this.up('form').getForm().reset();
    		        	store.getProxy().extraParams=form.getValues();
    		        	store.reload();
    		        	alert("Button Click Success");
                        console.log('reset');
    		        }
    		        
    		    },

                 {
///////////////////////search button calling the proxy //////////////////////////                 
                    xtype:'button',
                    text:"Delete Entries",
                    margin: '10px 10px 10px 600px',
                    handler: function(){
                         popup.show();
                    }
                    
                }
    ]};



        var popup = new Ext.Panel({
            floating: true,
            centered: true,
            modal: true,
            width: 300,
            height: 400,
            styleHtmlContent: true,
            html: '<p align ="center"><img src = "https://4.imimg.com/data4/PC/NV/MY-2918998/warning-sign-500x500.jpg " height="100" width="100"></p></br><p>You are going to delete the entire content in db.</p><p>The action cannot be reverted </p><p>Proceed at your own risk</p>',
            dockedItems: [{
                xtype: 'toolbar',
                title: 'PopUp',
                items: [{
                    xtype: 'button',
                    text:"Proceed",
                    handler: function(){
                      popup.hide();

                       var user = Ext.create('deleteAll', {value:'True'});
                       user.save(); 
                       store.reload();
                       grid.getView().refresh()

                      console.log('deleted');
                    }
                },{
                    text: 'Cancel',
                    handler: function(){
                        popup.hide();
                    }
                }]
            }]
        });





 var button2={
             items: [
              

                 {
///////////////////////search button calling the proxy //////////////////////////                 
                    xtype:'button',
                    text:"Start Scan",
                    margin: '10px 10px 10px 100px',
                    handler: function(){
                        var form = this.up('form').getForm(); 
                        store.getProxy().extraParams=form.getValues();
                        this.up('form').getForm().reset();
                        store.reload();
                        console.log('scan');
                    }
                    
                }
    ]};


////////////////////creating the form pannel ///////////////////////////////////    
    var panel2 =new Ext.FormPanel({
          xtype: 'fieldset',
          title: 'Scan an Entire Directory',
          width:'100%',
          layout: 'vbox',
          
///////////////////add items to the form ////////////////////////////
    items: [textfeilds2,button2],
    renderTo: Ext.getBody()
    })



    var panel =new Ext.FormPanel({
    	  xtype: 'fieldset',
          title: 'Search Scanned Items',
          width:'100%',
          layout: 'vbox',
          
///////////////////add items to the form ////////////////////////////
    items: [textfeilds,comboxes,buttons,grid],
    renderTo: Ext.getBody()
    })



    console.log('end');
});