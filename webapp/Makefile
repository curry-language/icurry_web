PROGNAME = icurry_web

ROOT = $(CURDIR)

# The Curry Package Manager used to install the ICurry interpreter
#CPM = /opt/pakcs/bin/cypm
CPM = /opt/kics2/bin/cypm

LOGDIR  = LOG
LOGFILE = $(LOGDIR)/production.log
PIDFILE = server.pid

PID := $(shell if [ -f $(PIDFILE) ] ; then cat $(PIDFILE) ; else echo "" ; fi)

SERVERADDRESS = 127.0.0.1
# The port number to be used by the local server
SERVERPORT = 13254

# Command to run the server:
SERVERCMD = flask --app icurry_web.py run -p $(SERVERPORT)

.PHONY: all
all:
	@echo "build start stop restart status ?"

.PHONY: build
build: icurry

# Build the binary of the ICurry interpreter
icurry:
	/bin/rm -f $(HOME)/.cpmrc # to avoid conflicts
	$(CPM) update
	$(CPM) --define BIN_INSTALL_PATH=$(ROOT) install icurry

.PHONY: start
start:
	@mkdir -p $(LOGDIR)
ifeq ($(PID),)
	@echo "Starting $(PROGNAME) on $(shell hostname --long)"
	nohup $(SERVERCMD) > $(LOGFILE) 2>&1 &
	@/bin/rm -f TMPOUT
	@ps x | grep flask > TMPOUT
	@grep python TMPOUT | awk '{ print $$1 }' > $(PIDFILE)
	@/bin/rm -f TMPOUT
	@echo "Started $(PROGNAME) on http://$(SERVERADDRESS):$(SERVERPORT)"
else
	@echo "$(PROGNAME) is already running with PID $(PID)."
endif

.PHONY: stop
stop:
ifeq ($(PID),)
	@echo "$(PROGNAME) is not running."
else
	@echo "Stopping $(PROGNAME)"
	ps -p $(PID) && kill -9 $(PID) 
	/bin/rm -f $(PIDFILE)
endif

.PHONY: restart
restart:
	$(MAKE) stop
	$(MAKE) start

.PHONY: status
status:
ifeq ($(PID),)
	@echo "$(PROGNAME) is not running."
else
	@echo "$(PROGNAME) is running with PID $(PID):"
	ps -p $(PID)
endif
