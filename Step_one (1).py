# -*- encoding: utf-8 -*-
from odoo import models, fields, api,_,exceptions,tools
from odoo.exceptions import UserError, AccessError, ValidationError, DeferredException
from odoo.http import request
import erppeek
import odoorpc
import sys,os
from multiprocessing.sharedctypes import template
import datetime
from xmlrpclib import ServerProxy
from pychart.arrow import default
import paramiko
import sys
reload(sys)
import base64
import logging
_logger = logging.getLogger(__name__)

SERVER = 'http://localhost:8073'








 




############# AJOUT DUNE INSTANCE ####################

class Firststep(models.Model):
    _name = 'step.step'
    _description = 'First step'
    
    

    

    
    db_name = fields.Char(required=True,string=u"الإسم التقني")  
    db_password = fields.Char(required=True,string=u"كلمة المرور")
    db_login = fields.Char(required=True,string=u"المستخدم")
    confirm_password = fields.Char(required=True,string=u"تأكيد كلمة المرور")
    Attempt_id = fields.One2many('test2','attendee_ids')
    date = fields.Date(default=fields.Date.today ,readonly=True)
    state = fields.Boolean(string=u'مفعل',default=True)
    
    
    @api.model
    def create(self,vals):
        res=super(Firststep, self).create(vals)
        res.db_create()
        return res
    
    @api.multi
    def unlink(self):

        res = super(Firststep, self).unlink()
        return res   
        

   
    @api.constrains('db_password','confirm_password')
    def _check_something(self):
        for record in self:
            if self.confirm_password:
                
                if not (record.db_password == record.confirm_password):
                    raise ValidationError(u"كلمات المرور غير مطابقين: %s" % record.confirm_password)



  

    
    @api.multi
    def db_create(self): 


        client = erppeek.Client(server=SERVER)
        if self.db_name in client.db.list():
            raise UserError(_(u'هذا الاسم مستخدم!!!')) 
        else:         
            if self.db_name and self.db_login and self.db_password:
                try:
                    client.create_database('admin', self.db_name, demo=False, lang='en_US', user_password=self.db_password, login=self.db_login)
                except Exception as e:
                    msg = _('tnaa')

            
            
            
            
            



   
    
    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.db_name:
                result.append((record.id, record.db_name))

           
        return result   
    
    
 


 
    

                





            
            
        
      
                
        
        



    

              

    

    
    
         
    @api.model
    def Heaven(self):

        aa = self.env['step.step'].sudo().search_read()
 


        return aa  
    
    


class Secondste(models.Model):
    _name = 'scnd_step'
    _description = 'Second step'
    
         
   
   
   
    @api.multi
    def get_db_list(self):
        res =[]
       
        client = erppeek.Client(server=SERVER)
        db_list = client.db.list()
        for dbb in db_list:
            aa = (dbb,dbb)
            res.append(aa)
       
        return res 
    
    
 
    

      
        
    @api.multi
    def db_stop(self):
        ad = 'admin'
        SERVER1 = 'localhost'
        port = "8073" 
        bkp_dir = '/home/odoo/Bureau/test'
        timeout = 18000
        odoo = odoorpc.ODOO(SERVER1, port=port)


        if self.db_liste:
            Blue = str(self.db_liste.db_name)

            path = bkp_dir+Blue+'.zip'
            
            

            try: dump = odoo.db.dump(ad, Blue)
            except odoorpc.error.RPCError as e: 
                if str(e)!='Access denied': # database doesn't exist
                    odoo.config['timeout'] = timeout
                    sys.exit(0)
                else: raise e
            with open(path, 'wb') as dump_zip:
                dump_zip.write(dump.read())
              
            bb = open(path, 'rb')

            aa = base64.b64encode(bb.read())
     
            ATTACHMENT_NAME = "Taraji"
            self.env['ir.attachment'].create({
            'name': ATTACHMENT_NAME,
            'type': 'binary',
            'datas': aa,
            'datas_fname': ATTACHMENT_NAME + '.zip',
            'store_fname': ATTACHMENT_NAME,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-zip'
        })

            odoo.db.drop(ad, Blue)
            odoo.config['timeout'] = timeout
            query = """ UPDATE step_step SET state=%s WHERE db_name=%s
            
            """ 
            self._cr.execute(query, (False, aa)) 

 

             
        return True    


    name = fields.Char(string='Nom')
    

    @api.multi
    def db_restore(self):
        
        SERVER1 = 'localhost'
        port = "8073" 
        bkp_dir = '/home/odoo/Bureau/test'
        timeout = 18000
        odoo = odoorpc.ODOO(SERVER1, port=port) 
        master_password = 'admin'
        path = bkp_dir+self.name+'.zip'
        dump = open(path, 'rb')


        timeout_backup = odoo.config['timeout']
        odoo.config['timeout'] = timeout
        try: odoo.db.restore(master_password, self.name, dump)
        except odoorpc.error.RPCError as e: 
            if str(e)!='Access denied': # database already exists
                odoo.db.drop(master_password, self.name)
                odoo.db.restore(master_password, self.name, dump)
                os.remove(path)
            else: raise e
        finally: odoo.config['timeout'] = timeout_backup
        os.remove(path)   
    
   
       
   
   
   
    @api.multi
    def db_delete(self):
        if self.db_liste:
            
            aa = self.db_liste.db_name
            client = erppeek.Client(server=SERVER)
            delt = client.db.drop('admin', aa)
            if delt: 
                self._cr.execute("DELETE FROM step_step WHERE db_name=%s", (self.db_liste,))

            
            
       

              
        return True 
    
    @api.multi
    def Open_interface(self):
        
  
        

        
        action = self.env.ref('First_step.Step_one_act').read()[0]

        return action
        
    name = fields.Char(string='Base 1',default='Enn')   
    db_liste = fields.Many2one('step.step', string= u'قائمة المكتاب')

    
###################################33333  
    
    





class c(models.Model):
    _name = 'wahran' 
    


    login = fields.Char(string = 'login',default='Admin')
    password = fields.Char(string = 'password',default='0000')
    
    
    @api.multi
    def Crt(self):
        aa = self.env['dash.dashme']
        x = aa.Open_interface()


        
        return x
    
    
    @api.multi
    def Crt2(self):
        aa = self.env['dash.dashme']
        return True


        
    



class A(models.Model):
    _inherit = 'wahran' 

    type = fields.Char(string = 'hey you')



    @api.multi
    def db_restore(self):
        
        SERVER = 'localhost'
        port = "8073" 
        bkp_dir = '/home/odoo/Bureau/test'
        timeout = 18000
        odoo = odoorpc.ODOO(SERVER, port=port) 
        master_password = 'admin'
        path = bkp_dir+self.name+'.zip'
        dump = open(path, 'rb')


        timeout_backup = odoo.config['timeout']
        odoo.config['timeout'] = timeout
        try: odoo.db.restore(master_password, self.name, dump)
        except odoorpc.error.RPCError as e: 
            if str(e)!='Access denied': # database already exists
                odoo.db.drop(master_password, self.name)
                odoo.db.restore(master_password, self.name, dump)
                os.remove(path)
            else: raise e
        finally: odoo.config['timeout'] = timeout_backup
        os.remove(path) 





class B(models.Model):
    _name = 'test2' 
    
    inst_mod = fields.Char(string = 'Too',readonly=True)

    uns_mod = fields.Char(string = 'highway',readonly=True)
    attendee_ids = fields.Many2one('step.step', string="Attendees" , track_visibility='onchange') 
    


    @api.multi
    def open_wiz(self):
        
        res = []

        if self.attendee_ids:

            
            
            bb = self.attendee_ids.db_login
            aa = self.attendee_ids.db_name
            cc = self.attendee_ids.db_password
            client = erppeek.Client(SERVER,aa,bb,cc)

            
            installed_modules = client.modules([('application', '=', True)],installed=False)
            if installed_modules is None:
                raise ValidationError(u"لا يوجد تطبيقات في  %s" % aa)
            res = installed_modules.get('uninstalled')
            res.append(str(aa))
            res.append(str(bb))
            res.append(str(cc))


            Blue = str(res)
            Mod={
               'uns_mod' :Blue, } 

            self.env['test2'].sudo().create(Mod)
            self.env.cr.commit()



       


        self.ensure_one()
        action = self.env.ref('First_step.Step_wizard_action_view').read()[0]

        return action 
    
    
    @api.multi
    def open_wiz_des(self):
        
        res = []

        if self.attendee_ids:

            
            
            bb = self.attendee_ids.db_login
            aa = self.attendee_ids.db_name
            cc = self.attendee_ids.db_password
            client = erppeek.Client(SERVER,aa,bb,cc)

            
            installed_modules = client.modules([('application', '=', True)],installed=True)
            if installed_modules is None:
                raise ValidationError(u"لا يوجد تطبيقات في  %s" % aa)
            res = installed_modules.get('installed')
            res.append(str(aa))
            res.append(str(bb))
            res.append(str(cc))


            Blue = str(res)
            Mod={
               'inst_mod' :Blue, } 

            self.env['test2'].sudo().create(Mod)
            self.env.cr.commit()



       


        self.ensure_one()
        action = self.env.ref('First_step.Uni_wizard_action_view').read()[0]

        return action 


         





###################################################################
################"
########     

class Bakhta(models.Model):
    _name = 'hope.hope'



    @api.model
    def update_state(self):
        query = """ UPDATE step_step SET state=%s WHERE db_name=%s
            """
        
        client = erppeek.Client(server=SERVER)
        db_list = client.db.list()   
        aa =  self.env['step.step'].search([])
        for j in aa :
            if db_list.count(j['db_name']) <> 1: 
                self._cr.execute(query, (False, j['db_name'])) 



    @api.multi
    def Tester(self):
        res = []
        aa = self.env['step.step'].sudo().search_read()

            
           
        return res     


  
    @api.multi
    def dash_db(self):
        client1 = erppeek.Client(server=SERVER)
        listdb = client1.db.list()
        liste = []
        aa = self.env['step.step'].sudo().search([])
        for x in aa:
            if listdb.count(x.db_name) == 1:

                liste.append(x.db_name)
       

        


        return liste
    
    
    
    @api.multi
    def mod_number(self):
        a = 0
        liste = []
        listdb = []

        client1 = erppeek.Client(server=SERVER)
        listdb = client1.db.list()
        

        aa = self.env['step.step'].sudo().search([])
        for x in aa:
            if listdb.count(x.db_name) == 1:
            
                client2 = erppeek.Client(SERVER,x.db_name,x.db_login,x.db_password)
                
                installed_modules = client2.modules([('application', '=', True)],installed=True)
            #    liste.append(len(installed_modules))
                if installed_modules is None:
                    a = 0
                else:
                    a = len(installed_modules.get('installed'))
                liste.append(a)
            
            
        
        
      
                
        
        


        return liste



    @api.multi
    def get_all_module(self):
        bb = []


        aa = self.env['ir.module.module'].sudo().search([('application', '=', True)])
        for x in aa:
            bb.append(str(x.name))     
        
        
        return bb
   
    @api.multi
    def get_nbr_module(self):
        a = 0
        liste = []
        listdb = []
        client1 = erppeek.Client(server=SERVER)
        listdb = client1.db.list()
        

        aa = self.env['step.step'].sudo().search([])
        for x in aa:
            if listdb.count(x.db_name) == 1:
            
                client2 = erppeek.Client(SERVER,x.db_name,x.db_login,x.db_password)
                
                installed_modules = client2.modules([('application', '=', True)],installed=True)
            #    liste.append(len(installed_modules))
                if installed_modules is None:
                    a = 0
                else:
                    a = len(installed_modules.get('installed'))
                    b = self.get_all_modules()
                    
                liste.append(a)
            
        return liste
    
    
    
    @api.multi
    def get_date(self):
        res = []
        aa = self.env['step.step'].sudo().search_read()
        for x in aa:
            res.append(x['create_date'])
        
        
        return res



    @api.multi
    def Db_table(self):
       
        cr = self.env.cr
        query = """
            select db_name,State from step_step
        """
        cr.execute(query)
        res = cr.dictfetchall() 
       
        return res 
    

               
    @api.model
    @api.multi
    def maybe(self):
        aa =[]

        try: 
            aa = self.env['hope.hope'].sudo().search_read()
            a1 = self.dash_db()
            a2  =self.mod_number()
        
            a3 = self.get_all_module()
            a4 = self.get_users()
            a5 =self.get_date()
            a6 = self.Db_table()
            data = {
                'name1': a1,
                'name2': a2,
                'name3' : a3,
                'name4' : a4,
                'name5' : a5,
                'liste_bases' : a6,
                
                
            }
 
            aa[0].update(data)

        except Exception as e:
            msg = _('tnaa')
            
        return aa
    
    
    
    @api.multi
    def get_users(self):
        a = {}
        liste = []
        listdb = []
        client1 = erppeek.Client(server=SERVER)
        listdb = client1.db.list()
        

        aa = self.env['step.step'].sudo().search([])
        i = 0
        for x in aa:
            if listdb.count(x.db_name) == 1:

                server = ServerProxy('http://localhost:8073/xmlrpc/common')
                user_id = server.login(x.db_name, x.db_login, x.db_password)

                server = ServerProxy('http://localhost:8073/xmlrpc/object')
                user_ids = server.execute(x.db_name, user_id, x.db_password,'res.users', 'search', [])

                i = 0
                users = server.execute(x.db_name, user_id, x.db_password,'res.users', 'read', user_ids, [])

                for user in users:
                    i = i + 1
                liste.append(i)
        
                    

                
        return liste
      
    @api.multi
    def Open_interface(self):
        
        bb = self.env['wahran'].sudo().search_read()
        for record in self:
            
            if (record.login == str(bb[0]['login'])) and (record.password == str(bb[0]['password'])):
                aa = self.maybe()
                query = """ UPDATE step_step SET state=%s WHERE db_name=%s
            """
        
                client = erppeek.Client(server=SERVER)
                db_list = client.db.list()   
                aa =  self.env['step.step'].search([])
                for j in aa :
                    if db_list.count(j['db_name']) <> 1: 
                        self._cr.execute(query, (False, j['db_name'])) 
                    else :
                        self._cr.execute(query, (True, j['db_name'])) 
        
                query2 = """ DELETE  FROM test2
            """
                self._cr.execute(query2)
        

        
                action = self.env.ref('First_step.Step_one_act').read()[0]

                return action
                query3 = """ DELETE  FROM hope_hope WHERE id <> 0"""
                self._cr.execute(query3)
            else:
                raise ValidationError(u'يوجد خطأ فالبيانات')


               
            
            

                
        
        
    
    
    @api.multi
    def Open_res(self):

        query = """ UPDATE wahran SET login=%s,password=%s WHERE ID=1
            """
        import random
        from random import randint
        import string
        pas = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(randint(12,15)))
        self._cr.execute(query, ('Admin', pas)) 
        action = self.env.ref('hope.hope').read()[0]

        print(pas)
        return action


        
        
    
    name2 = fields.Char(string = 'Soussa')

    name1 = fields.Char(string = 'lallala')
    
    name3 = fields.Char(string = 'crzy')
    
    name4 = fields.Char(string = 'Liste users')
    
    name5 = fields.Char(string = 'Dates')
    
    login = fields.Char(string = 'Login')
    
    password = fields.Char(string = 'Password !')
    
    liste_bases = fields.Char(string = 'Liste des bases')


    ####################################################################
    
    
class Dashboar_data(models.Model):
    _name = 'dash.dashme' 
    

    list_db = fields.Char(string = 'liste')
    db_liste = fields.Many2one('step.step', string =u'قائمة المكتاب')
    attachment_ids = fields.Many2many('ir.attachment', 'class_ir_attachments_rel', 'class_id', 'attachment_id', 'Attachments')



    @api.multi
    def love(self):
        query = """ UPDATE wahran SET login=%s,password=%s WHERE ID=1
            """
        import random
        from random import randint
        import string
        pas = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(randint(12,15)))
        self._cr.execute(query, ('Admin', pas)) 

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.list_db:
                result.append((record.id, record.list_db))

           
        return result 
    
    
    @api.multi
    def db_restore(self):
        
        SERVER1 = 'localhost'
        port = "8073" 
        bkp_dir = '/home/odoo/Bureau/test'
        timeout = 18000
        odoo = odoorpc.ODOO(SERVER1, port=port) 
        master_password = 'admin'


        if self.db_liste:
            aa = str(self.db_liste.db_name)
            path = bkp_dir+aa+'.zip'
            dump = open(path, 'rb')
            
            timeout_backup = odoo.config['timeout']
            odoo.config['timeout'] = timeout
            try: odoo.db.restore(master_password, aa, dump)
            except odoorpc.error.RPCError as e: 
                if str(e)!='Access denied': # database already exists
                    odoo.db.drop(master_password, aa)
                    odoo.db.restore(master_password, aa, dump)
                    os.remove(path)
                else: raise e
            finally: odoo.config['timeout'] = timeout_backup
            os.remove(path)  
            query = """ UPDATE step_step SET state=%s WHERE db_name=%s
            
            """ 
            self._cr.execute(query, (True, aa)) 


    @api.multi
    def Open_interface(self):
        
  
        

        
        action = self.env.ref('First_step.Step_one_act').read()[0]

        return action

        
class adduser(models.Model):
    _name = 'add.user' 
    
    
    base_name = fields.Many2one('step.step',string =u"إسم المكتب")
    name = fields.Char(string = u"الاسم",required =True)
    mail = fields.Char(string = u"البريد الالكروني",required=True)
  
  
  
    @api.multi
    def create_user(self):
        if self.base_name and self.name and self.mail:
            base = self.base_name.db_name
            login = self.base_name.db_login
            password = self.base_name.db_password
            client = erppeek.Client(SERVER,base,login,password)
            model = client.model('res.users')
            values = {
                'name': self.name,
                'login': self.mail
               } 
            model.create(values)

            
       
        
        
        