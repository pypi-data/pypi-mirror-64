!function(){"use strict";try{self["workbox:sw:4.1.1"]&&_()}catch(t){}const t="https://storage.googleapis.com/workbox-cdn/releases/4.1.1",e={backgroundSync:"background-sync",broadcastUpdate:"broadcast-update",cacheableResponse:"cacheable-response",core:"core",expiration:"expiration",googleAnalytics:"offline-ga",navigationPreload:"navigation-preload",precaching:"precaching",rangeRequests:"range-requests",routing:"routing",strategies:"strategies",streams:"streams"};self.workbox=new class{constructor(){return this.v={},this.t={debug:"localhost"===self.location.hostname,modulePathPrefix:null,modulePathCb:null},this.s=this.t.debug?"dev":"prod",this.o=!1,new Proxy(this,{get(t,s){if(t[s])return t[s];const o=e[s];return o&&t.loadModule(`workbox-${o}`),t[s]}})}setConfig(t={}){if(this.o)throw new Error("Config must be set before accessing workbox.* modules");Object.assign(this.t,t),this.s=this.t.debug?"dev":"prod"}loadModule(t){const e=this.i(t);try{importScripts(e),this.o=!0}catch(s){throw console.error(`Unable to import module '${t}' from '${e}'.`),s}}i(e){if(this.t.modulePathCb)return this.t.modulePathCb(e,this.t.debug);let s=[t];const o=`${e}.${this.s}.js`,r=this.t.modulePathPrefix;return r&&""===(s=r.split("/"))[s.length-1]&&s.splice(s.length-1,1),s.push(o),s.join("/")}}}();
//# sourceMappingURL=workbox-sw.js.map
