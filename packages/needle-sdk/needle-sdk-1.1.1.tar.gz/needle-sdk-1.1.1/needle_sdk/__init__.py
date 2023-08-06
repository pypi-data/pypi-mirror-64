# Copyright (c) 2020, Varlogix Technologies
# All rights reserved.
# Our terms: https://needle.sh/terms

_l=')\\b'
_k='\\b('
_j='Error while sending req data'
_i='errors'
_h='user_agent'
_g='platform'
_f='test_mode'
_e='app_id'
_d='basic'
_c='modules_used'
_b='path'
_a='django'
_Z='api_key'
_Y='Error checking command injection'
_X='pymongo.find'
_W='os.popen'
_V='os.system'
_U='psycopg2.connect'
_T='mysql.connector.connect'
_S='django.template.loader.render_to_string'
_R='django.core.handlers.base.BaseHandler.get_response'
_Q='#'
_P='action'
_O='|'
_N='scan'
_M='block'
_L='name'
_K='framework'
_J='active'
_I='type'
_H='value'
_G='mdbi'
_F='xss'
_E='cmdi'
_D='sqli'
_C=None
_B=True
_A=False
import requests,json,time,threading,platform,re,importlib
class RequestData:data=[];remote_addr='';request_method='';http_host='';path_info='';http_user_agent='';incident_action='';incident_module=''
class InstrMethod:sec_module='';py_module='';orig_method=_C;is_instr=_A
class NeedleApp:
	agent_version='';app_id='';api_key='';server_url='';platform='python';framework='';project_dir='';settings={};app_active=_A;errors=[];total_requests=0;mal_requests=[];modules_used=[];test_mode=_A;debug_mode=_A;instr_list=[];is_instr=_A;libinjec=_C;xss_pattern=_C;cmdi_pattern=_C;mdbi_pattern=_C;scan_pattern=_C;orig_sql_cursor_execute=_C;show_blocked_message=_A;use_libinjec=_B
	def __init__(A,debug):
		I='='
		if A.detect_framework():A.debug_mode=debug
		else:print('Needle.sh error: Web framework not supported. Stopping agent.');return
		try:
			E=A.project_dir+'/needle_settings.ini'
			with open(E)as F:
				for (J,D) in enumerate(F):
					if D[0]!=_Q:
						C,B=D.strip().split(I)
						if C==_e:A.app_id=B
						if C==_Z:A.api_key=B
						if C=='server_url':A.server_url=B
						if C==_f:
							if B=='0':A.test_mode=_A
							elif B=='1':A.test_mode=_B;print('Needle.sh: Agent in Test Mode...')
						if A.debug_mode:print(C,I,B)
		except Exception as G:H=str(G);A.add_error('Error opening settings INI file',H)
		if A.app_id==''or A.api_key=='':print('Needle.sh error: App ID or API key incorrect. Stopping agent.');return
	def detect_framework(A):
		B=_A
		try:from django.conf import settings as C;A.framework=_a;A.project_dir=C.BASE_DIR;B=_B
		except Exception as D:pass
		return B
	def add_error(A,error,error_data):
		B=error
		if A.debug_mode:print('Needle.sh: Error! ',B)
		A.errors.append({_g:A.platform,'error':B,'error_data':error_data})
	def add_mal_request(C,action,reason,arg_type,arg_name,arg_value,req_data):
		E=arg_value;D=arg_name;B=req_data;D,E=C.check_sensitive_data(D,E);A={};A[_I]=action;A['reason']=reason;A['arg_type']=arg_type;A['arg_name']=D;A['arg_value']=E;A['client_ip']=B.remote_addr;A['http_method']=B.request_method;A['server']=B.http_host;A[_b]=B.path_info;A[_h]=B.http_user_agent
		if C.debug_mode:print('Needle.sh: Adding incident: ',A)
		C.mal_requests.append(A)
	def add_module(A,type,package,method):
		B={_I:type,'package':package,'method':method}
		if not B in A.modules_used:A.modules_used.append(B)
	def api_thread(A):
		B=0;C=0;D=0
		try:
			while _B:
				if B==0:A.api_get_settings()
				if A.app_active and(A.total_requests>0 or len(A.mal_requests)>0):A.api_send_req_data()
				if A.app_active and C==0 and len(A.errors)>0:A.api_send_app_info(_i)
				if A.app_active and D==0 and len(A.modules_used)>0:A.api_send_app_info(_c)
				B+=1;C+=1;D+=1
				if B==1:B=0
				if C==1:C=0
				if D==10:D=0
				time.sleep(30)
		except Exception as E:F=str(E);A.add_error(_j,F)
	def get_api_payload(A):
		B=0
		if A.test_mode:B=1
		C=0
		if A.get_libinjec():C=1
		D={_e:A.app_id,_Z:A.api_key,_f:B,'libinjec':C,_g:A.platform,_K:A.framework,'agent_version':A.agent_version};return D
	def api_send_app_info(A,info):
		if A.debug_mode:print('Needle.sh: Sending app info data')
		try:
			C=A.server_url+'/api/store_app_info';B=A.get_api_payload()
			if info==_i and len(A.errors)>0:B['agent_errors']=A.errors;A.errors=[]
			if info==_c and len(A.modules_used)>0:B[_c]=A.modules_used;A.modules_used=[]
			D=json.dumps(B);G=requests.post(C,data=D)
		except Exception as E:F=str(E);A.add_error('Error while sending app info',F)
	def api_send_req_data(A):
		J='total_requests';D='mal_requests'
		if A.debug_mode:print('Needle.sh: Sending requests data')
		try:
			E=A.server_url+'/api/store_requests';B=A.get_api_payload()
			if A.total_requests>0:B[J]=A.total_requests;A.total_requests=0
			if len(A.mal_requests)>0:B[D]=A.mal_requests;A.mal_requests=[]
			F=json.dumps(B);K=requests.post(E,data=F)
		except Exception as G:
			H=str(G);A.add_error(_j,H);A.total_requests+=B[J]
			if len(B[D])>0:C=B[D];I=A.mal_requests;C.extend(I);A.mal_requests=C
	def api_get_settings(A):
		if A.debug_mode:print('Needle.sh: Getting app settings')
		try:
			E=A.server_url+'/api/get_app_settings';F=A.get_api_payload();G=json.dumps(F);D=requests.post(E,data=G)
			if A.debug_mode:print('Needle.sh: Received app settings = ',D.text)
			H=json.loads(D.text);A.settings=H['settings']
		except Exception as B:C=str(B);A.add_error('Error while fetching settings',C)
		try:
			if A.settings[_J]==1:
				A.app_active=_B;A.instrument(_d,_B)
				if _D in A.settings and A.settings[_D][_J]==1:A.instrument(_D,_B)
				else:A.instrument(_D,_A)
				if _F in A.settings and A.settings[_F][_J]==1:A.instrument(_F,_B)
				else:A.instrument(_F,_A)
				if _E in A.settings and A.settings[_E][_J]==1:A.instrument(_E,_B)
				else:A.instrument(_E,_A)
				if _G in A.settings and A.settings[_G][_J]==1:A.instrument(_G,_B)
				else:A.instrument(_G,_A)
			elif A.settings[_J]==0:A.app_active=_A;A.instrument(_d,_A);A.instrument(_D,_A);A.instrument(_F,_A);A.instrument(_E,_A);A.instrument(_G,_A)
		except Exception as B:C=str(B);A.add_error('Error while instrumenting',C)
	def update_instr_status(B,sec_module,py_module,orig_method,is_instr):
		E=py_module;D=sec_module;C=is_instr;F=_A
		for (H,G) in enumerate(B.instr_list):
			if G.sec_module==D and G.py_module==E:F=_B;B.instr_list[H].is_instr=C;break
		if not F:A=InstrMethod();A.sec_module=D;A.py_module=E;A.orig_method=orig_method;A.is_instr=C;B.instr_list.append(A)
		return C
	def get_module_status(C,py_module):
		A=_A
		for B in C.instr_list:
			if B.py_module==py_module and B.is_instr:A=_B;break
		return A
	def get_orig_method(B,py_module):
		for A in B.instr_list:
			if A.py_module==py_module:return A.orig_method
	def is_module_installed(B,module):A=importlib.find_loader('spam');C=A is not _C
	def instrument(C,sec_module,is_instr):
		M=is_instr;J=sec_module;E='py_module';D='sec_module';N=[{D:_d,_K:_a,E:_R},{D:_F,_K:_a,E:_S},{D:_D,_K:'',E:_T},{D:_D,_K:'',E:_U},{D:_E,_K:'',E:_V},{D:_E,_K:'',E:_W},{D:_G,_K:'',E:_X}]
		for F in N:
			if F[D]!=J:continue
			if F[_K]!=''and F[_K]!=C.framework:continue
			A=F[E]
			if M!=C.get_module_status(A):
				if M:
					if C.debug_mode:print('Instrumenting sec module:',A)
					try:
						B=''
						if A==_R:
							try:from django.core.handlers.base import BaseHandler as G;B=G.get_response;G.get_response=needle_django_get_response
							except ImportError:pass
						if A==_S:
							try:import django.template.loader;B=django.template.loader.render_to_string;django.template.loader.render_to_string=needle_django_template_render
							except ImportError:pass
						if A==_T:
							try:import mysql.connector;B=mysql.connector.connect;mysql.connector.connect=needle_mysql_connect
							except ImportError:pass
						if A==_U:
							try:import psycopg2 as H;B=H.connect;H.connect=needle_psycopg2_connect
							except ImportError:pass
						if A==_V:
							try:import os;B=os.system;os.system=needle_os_system
							except ImportError:pass
						if A==_W:
							try:import os;B=os.popen;os.popen=needle_os_popen
							except ImportError:pass
						if A==_X:
							try:from pymongo.collection import Collection as I;B=I.find;I.find=needle_mongo_find
							except ImportError:pass
						C.update_instr_status(J,A,B,_B)
					except Exception as K:L=str(K);C.add_error('Error while instrumenting module: '+A,L)
				else:
					try:
						B=''
						if A==_R:
							try:from django.core.handlers.base import BaseHandler as G;B=C.get_orig_method(A);G.get_response=B
							except ImportError:pass
						if A==_S:
							try:import django.template.loader;B=C.get_orig_method(A);django.template.loader.render_to_string=B
							except ImportError:pass
						if A==_T:
							try:import mysql.connector;B=C.get_orig_method(A);mysql.connector.connect=B
							except ImportError:pass
						if A==_U:
							try:import psycopg2 as H;B=C.get_orig_method(A);H.connect=B
							except ImportError:pass
						if A==_V:
							try:import os;B=C.get_orig_method(A);os.system=B
							except ImportError:pass
						if A==_W:
							try:import os;B=C.get_orig_method(A);os.popen=B
							except ImportError:pass
						if A==_X:
							try:from pymongo.collection import Collection as I;B=C.get_orig_method(A);I.find=B
							except ImportError:pass
						C.update_instr_status(J,A,B,_A)
					except Exception as K:L=str(K);C.add_error('Error while un-instrumenting module: '+A,L)
	def get_sec_headers(A):
		H='h_ref';G='h_mime';F='h_xss';E='h_cj';B={}
		try:
			if A.app_active:
				if E in A.settings:B['X-Frame-Options']=A.settings[E]
				if F in A.settings:B['X-XSS-Protection']=A.settings[F]
				if G in A.settings:B['X-Content-Type-Options']=A.settings[G]
				if H in A.settings:B['Referrer-Policy']=A.settings[H]
		except Exception as C:D=str(C);A.add_error('Error getting security headers: ',D)
		return B
	def xss_module_active(A):
		B=_A;C=''
		try:
			if A.app_active and _F in A.settings and A.settings[_F][_J]==1:B=_B;C=A.settings[_F][_P]
		except Exception as D:E=str(D);A.add_error('Error checking module active: xss: ',E)
		return B,C
	def cmdi_module_active(A):
		B=_A;C=''
		try:
			if A.app_active and _E in A.settings and A.settings[_E][_J]==1:B=_B;C=A.settings[_E][_P]
		except Exception as D:E=str(D);A.add_error('Error checking module active: cmdi: ',E)
		return B,C
	def sqli_module_active(A):
		B=_A;C=''
		try:
			if A.app_active and _D in A.settings and A.settings[_D][_J]==1:B=_B;C=A.settings[_D][_P]
		except Exception as D:E=str(D);A.add_error('Error checking module active: sqli: ',E)
		return B,C
	def mdbi_module_active(A):
		B=_A;C=''
		try:
			if A.app_active and _G in A.settings and A.settings[_G][_J]==1:B=_B;C=A.settings[_G][_P]
		except Exception as D:E=str(D);A.add_error('Error checking module active: mdbi: ',E)
		return B,C
	def scan_module_active(A):
		B=_A;C=''
		try:
			if A.app_active and _N in A.settings and A.settings[_N][_J]==1:B=_B;C=A.settings[_N][_P]
		except Exception as D:E=str(D);A.add_error('Error checking module active: scan: ',E)
		return B,C
	def get_libinjec(A):
		G='Error getting libinjec module for platform: '
		if not A.use_libinjec:return _C
		try:
			if A.libinjec:return A.libinjec
			if not A.libinjec:
				B=_C;C=platform.system()
				if C=='Darwin':from needle_sdk.libinjection2.mac_x86_64 import libinjection as D;B=D
				elif C=='Linux':from needle_sdk.libinjection2.linux import libinjection as D;B=D
				elif C=='':A.add_error(G,'Unrecognised platform')
				A.libinjec=B;return A.libinjec
		except Exception as E:F=str(E);A.add_error(G,F);return _C
	def get_xss_pattern(B):
		try:
			if B.xss_pattern:return B.xss_pattern
			else:
				import os,sys,inspect as D;E=os.path.dirname(os.path.abspath(D.getfile(D.currentframe())));F=E+'/js_event_list';A=''
				with open(F)as G:
					for (K,C) in enumerate(G):
						C=C.strip()
						if C==''or C[0]==_Q:continue
						A+=C+_O
				A=A.rstrip(_O);A=_k+A+_l;A='(<[\\\\s]*script[\\\\s]*[>]*|javascript:|javascript&colon;|FSCommand)|'+A;H=re.compile(A,re.IGNORECASE);B.xss_pattern=H;return B.xss_pattern
		except Exception as I:J=str(I);B.add_error('Error getting XSS pattern:',J);return _C
	def get_cmdi_pattern(B):
		try:
			if B.cmdi_pattern:return B.cmdi_pattern
			else:
				import os,sys,inspect as D;E=os.path.dirname(os.path.abspath(D.getfile(D.currentframe())));F=E+'/unix_cmd_list';A=''
				with open(F)as G:
					for (K,C) in enumerate(G):
						C=C.strip()
						if C==''or C[0]==_Q:continue
						A+=C.rstrip('+')+_O
				A=A.rstrip(_O);A='(^|\\s|;|&&|\\|\\||&|\\|)('+A+')($|\\s|;|&&|\\|\\||&|\\||<)|(\\*|\\?)';H=re.compile(A,re.IGNORECASE);B.cmdi_pattern=H;return B.cmdi_pattern
		except Exception as I:J=str(I);B.add_error('Error getting cmdi pattern:',J);return _C
	def get_mdbi_pattern(A):
		try:
			if A.mdbi_pattern:return A.mdbi_pattern
			else:B='\\$(?:ne|eq|lte?|gte?|n?in|mod|all|size|exists|type|slice|x?or|div|like|between|and|where|comment)';C=re.compile(B,re.IGNORECASE);A.mdbi_pattern=C;return A.mdbi_pattern
		except Exception as D:E=str(D);A.add_error('Error getting mdbi pattern:',E);return _C
	def get_scanner_pattern(B):
		try:
			if B.scan_pattern:return B.scan_pattern
			else:
				import os,sys,inspect as D;E=os.path.dirname(os.path.abspath(D.getfile(D.currentframe())));F=E+'/scanners_list';A=''
				with open(F)as G:
					for (K,C) in enumerate(G):
						C=C.strip()
						if C==''or C[0]==_Q:continue
						A+=C.rstrip('+')+_O
				A=A.rstrip(_O);A=_k+A+_l;H=re.compile(A,re.IGNORECASE);B.scan_pattern=H;return B.scan_pattern
		except Exception as I:J=str(I);B.add_error('Error getting scan pattern:',J);return _C
	def get_project_modules(C):
		try:
			import sys;D=sys.modules.keys();A=[]
			for E in D:
				B=E.split('.')
				if B[0]not in A:A.append(B[0])
		except Exception as F:G=str(F);C.add_error('Error getting module list',G)
	def get_blocked_page_content(D,module_id=''):
		B=module_id;C=''
		if D.show_blocked_message:
			A=''
			if B==_D:A='SQL injection'
			if B==_F:A='Cross-site Scripting(XSS)'
			if B==_E:A='Command injection'
			if B==_G:A='MongoDB injection'
			if B==_N:A='Security scanner'
			C='Blocked by Needle.sh! Attack type: '+A
		return C
	def check_sensitive_data(D,arg_name,arg_value):
		C=arg_name;A=arg_value
		try:
			import re;B='(\\d[ -]*){13,16}';B=re.compile(B,re.IGNORECASE);E=['password','passwd',_Z,'apikey','access_token','secret','authorization']
			if len(B.findall(A))>0 or C in E:A='[Sensitive data removed by Needle.sh]'
		except Exception as F:G=str(F);D.add_error('Error while checking sensitive data',G)
		return C,A
def needle_django_get_response(*A,**J):
	K=_R;global needle_app
	try:
		needle_app.total_requests+=1;B=RequestData();E=[]
		for (C,D) in A[1].GET.items():E.append({_I:'get',_L:C,_H:D})
		for (C,D) in A[1].POST.items():E.append({_I:'post',_L:C,_H:D})
		L=A[1].path.split('/')
		for M in L:E.append({_I:_b,_L:_b,_H:M})
		B.data=E;B.remote_addr=A[1].META['REMOTE_ADDR'];B.request_method=A[1].META['REQUEST_METHOD'];B.http_host=A[1].META['HTTP_HOST'];B.path_info=A[1].META['PATH_INFO'];B.http_user_agent=A[1].META['HTTP_USER_AGENT'];needle_data.req_data=B
		try:
			N,H=needle_app.scan_module_active()
			if N:
				O,P,Q,R=check_sec_scanner()
				if O:
					if needle_app.debug_mode:print('Needle.sh: New Incident of type: Security scanner')
					needle_data.req_data.incident_action=H;needle_data.req_data.incident_module=_N;needle_app.add_mal_request(H,_N,P,Q,R,needle_data.req_data)
		except Exception as F:G=str(F);needle_app.add_error('Error checking security scanner',G)
		I=needle_app.get_orig_method(K)(*A,**J);S=needle_app.get_sec_headers()
		for (T,(C,D)) in enumerate(S.items()):I[C]=D
		return I
	except Exception as F:G=str(F);needle_app.add_error('Error while adding request data to thread storage',G)
def check_content_xss(content):
	M='Error checking XSS:';G=content;global needle_app;B=_A;C='';D='';E=''
	try:
		H=needle_app.get_libinjec()
		for A in needle_data.req_data.data:
			F=A[_H]
			if F=='':continue
			if H:
				J=H.xss(F)
				if J==1:
					if G.find(F)>-1:B=_B;C=A[_I];D=A[_L];E=A[_H];return B,C,D,E
			else:
				print('Checking XSS using regex...');I=needle_app.get_xss_pattern()
				if I:
					if len(I.findall(F))>0:
						if G.find(F)>-1:B=_B;C=A[_I];D=A[_L];E=A[_H];return B,C,D,E
				else:needle_app.add_error(M,'XSS pattern unavailable')
	except Exception as K:L=str(K);needle_app.add_error(M,L)
	return B,C,D,E
def needle_django_template_render(*C,**D):
	E=_S;global needle_app
	try:
		needle_app.add_module(_F,'django.template.loader','render_to_string');A=needle_app.get_orig_method(E)(*C,**D)
		if needle_data.req_data.incident_action==_M:A=needle_app.get_blocked_page_content(needle_data.req_data.incident_module)
		F,B=needle_app.xss_module_active()
		if F:
			print('Checking XSS...');G,H,I,J=check_content_xss(A)
			if G:
				if needle_app.debug_mode:print('Needle.sh: New Incident of type: XSS')
				if B==_M:A=needle_app.get_blocked_page_content(_F)
				needle_app.add_mal_request(B,_F,H,I,J,needle_data.req_data)
		return A
	except Exception as K:L=str(K);needle_app.add_error('Error checking reflected XSS',L)
def check_command_injection(command):
	C=command;global needle_app;D=_A;E='';F='';G=''
	try:
		H=needle_app.get_cmdi_pattern()
		if H:
			for B in needle_data.req_data.data:
				A=B[_H]
				if A=='':continue
				J=["'",'"','\\','$@','`']
				for I in J:A=A.replace(I,'');C=C.replace(I,'')
				if A=='':continue
				if len(H.findall(A))>0:
					if C.find(A)>-1:D=_B;E=B[_I];F=B[_L];G=B[_H];return D,E,F,G
		else:needle_app.add_error('Error checking command injection:','Unavailable cmdi pattern')
	except Exception as K:L=str(K);needle_app.add_error(_Y,L)
	return D,E,F,G
def needle_cmdi_check(py_module,*A,**D):
	B=py_module;global needle_app;needle_app.add_module(_E,'',B)
	try:
		E,C=needle_app.cmdi_module_active()
		if E:
			F,G,H,I=check_command_injection(A[0])
			if F:
				if needle_app.debug_mode:print('Needle.sh: New Incident of type: Command injection')
				if C==_M:A='',;needle_data.req_data.incident_action=_M;needle_data.req_data.incident_module=_E
				needle_app.add_mal_request(C,_E,G,H,I,needle_data.req_data)
	except Exception as J:K=str(J);needle_app.add_error(_Y,K)
	return needle_app.get_orig_method(B)(*A,**D)
def needle_os_system(*A,**B):
	try:C=_V;return needle_cmdi_check(C,*A,**B)
	except Exception as D:E=str(D);needle_app.add_error(_Y,E)
def needle_os_popen(*A,**B):
	try:C=_W;return needle_cmdi_check(C,*A,**B)
	except Exception as D:E=str(D);needle_app.add_error(_Y,E)
def check_sql_injection(query):
	global needle_app;B=_A;C='';D='';E='';print('Checking SQL injection...')
	try:
		G=needle_app.get_libinjec()
		for A in needle_data.req_data.data:
			F=A[_H]
			if F=='':continue
			if G:
				H=G.sqli(F,'')
				if H==1:
					if query.find(F)>-1:B=_B;C=A[_I];D=A[_L];E=A[_H];needle_data.req_data.incident_action=_M;needle_data.req_data.incident_module=_D;return B,C,D,E
			else:
				I=re.compile('\\b(select|update|insert|alter|create|drop|delete|merge|union|show|exec|or|and|order|sleep|having)\\b|(&&|\\|\\|)',re.IGNORECASE)
				if len(F.split())>1 and len(I.findall(F))>0:B=_B;C=A[_I];D=A[_L];E=A[_H];needle_data.req_data.incident_action=_M;needle_data.req_data.incident_module=_D;return B,C,D,E
	except Exception as J:K=str(J);needle_app.add_error('Error checking SQL injection:',K)
	return B,C,D,E
def needle_sql_cursor_execute(*A,**C):
	global needle_app;needle_app.add_module(_D,'mysql.connection.cursor','execute')
	try:
		D,B=needle_app.sqli_module_active()
		if D:
			E,F,G,H=check_sql_injection(A[0])
			if E:
				if needle_app.debug_mode:print('Needle.sh: New Incident of type: SQL injection')
				if B==_M:A='-- Query blocked by Needle.sh agent (Possible SQL injection)',
				needle_app.add_mal_request(B,_D,F,G,H,needle_data.req_data)
	except Exception as I:J=str(I);needle_app.add_error('Error checking SQL injection',J)
	return needle_app.orig_sql_cursor_execute(*A,**C)
class NeedleSqlCursor:
	def __init__(A,cursor):
		try:A.cursor=cursor;needle_app.orig_sql_cursor_execute=A.cursor.execute;A.execute=needle_sql_cursor_execute
		except Exception as B:C=str(B);needle_app.add_error('Error initialising cursor object:',C)
	def __getattr__(A,name):
		try:return getattr(A.cursor,name)
		except Exception as B:C=str(B);needle_app.add_error('Error returning custom cursor method:',C)
class NeedleSqlConnection:
	def __init__(A,connection):
		try:A.connection=connection
		except Exception as B:C=str(B);needle_app.add_error('Error initialising custom SQL connection object:',C)
	def cursor(A,*B,**C):
		try:D=A.connection.cursor(*B,**C);return NeedleSqlCursor(D)
		except Exception as E:F=str(E);needle_app.add_error('Error getting cursor object from SQL connection:',F)
	def __getattr__(A,name):
		try:return getattr(A.connection,name)
		except Exception as B:C=str(B);needle_app.add_error('Error returning custom connection method:',C)
def needle_mysql_connect(*A,**B):
	C=_T;global needle_app
	try:D=needle_app.get_orig_method(C)(*A,**B);return NeedleSqlConnection(D)
	except Exception as E:F=str(E);needle_app.add_error('Error in instrumented MySQL connect:',F)
def needle_psycopg2_connect(*A,**B):
	C=_U;global needle_app
	try:D=needle_app.get_orig_method(C)(*A,**B);return NeedleSqlConnection(D)
	except Exception as E:F=str(E);needle_app.add_error('Error in instrumented psycopg2 connect:',F)
def check_mongodb_injection(query):
	L=':';G=query;global needle_app;A=_A;B='';C='';D=''
	if needle_app.debug_mode:print('Checking MongoDB injection...')
	try:
		I=needle_app.get_mdbi_pattern()
		if not I:return A,B,C,D
		H=''
		if isinstance(G,dict):H=json.dumps(G,separators=(',',L))
		else:H=G
		for E in needle_data.req_data.data:
			F=E[_H]
			if F=='':continue
			if len(F.split(L))>1 and len(I.findall(F))>0 and H.find(F)>-1:A=_B;B=E[_I];C=E[_L];D=E[_H];return A,B,C,D
	except Exception as J:K=str(J);needle_app.add_error('Error checking MongoDB injection:',K)
	return A,B,C,D
def needle_mongo_find(*D,**E):
	F=_X;global needle_app;needle_app.add_module(_G,'pymongo.collection','find')
	try:
		G,A=needle_app.mdbi_module_active()
		if G:
			H,I,J,K=check_mongodb_injection(D[1])
			if H:
				if needle_app.debug_mode:print('Needle.sh: New Incident of type: MongoDB injection')
				needle_data.req_data.incident_action=A;needle_data.req_data.incident_module=_G;needle_app.add_mal_request(A,_G,I,J,K,needle_data.req_data)
				if A==_M:return[]
	except Exception as B:C=str(B);needle_app.add_error('Error checking MongoDB injection',C)
	try:return needle_app.get_orig_method(F)(*D,**E)
	except Exception as B:C=str(B);needle_app.add_error('Error in instrumented pymongo.find:',C)
def check_sec_scanner():
	global needle_app;A=_A;B='';C='';D=''
	if needle_app.debug_mode:print('Checking Security scanner...')
	try:
		F=needle_app.get_scanner_pattern()
		if not F:return A,B,C,D
		E=needle_data.req_data.http_user_agent
		if E=='':return A,B,C,D
		if len(F.findall(E))>0:A=_B;B='http_header';C=_h;D=E;return A,B,C,D
	except Exception as G:H=str(G);needle_app.add_error('Error checking security scanner:',H)
	return A,B,C,D
def needle_start(debug=_A,show_blocked_message=_A):
	print('Needle.sh: Starting SDK (version'+g_sdk_version+')');global needle_app;needle_app=NeedleApp(debug);needle_app.agent_version=g_sdk_version;needle_app.show_blocked_message=show_blocked_message
	try:A=threading.Thread(target=needle_app.api_thread,args=(),daemon=_B);A.start()
	except Exception as B:C=str(B);needle_app.add_error('Error starting Wally thread to send data',C)
needle_app=_C
needle_data=threading.local()
g_sdk_version='1.1.1'