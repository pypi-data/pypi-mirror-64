(self.webpackJsonp=self.webpackJsonp||[]).push([[237],{852:function(t,e,n){"use strict";n.r(e);var r=n(12);function o(t){return(o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t})(t)}function i(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}function c(t,e){return!e||"object"!==o(e)&&"function"!=typeof e?function(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}(t):e}function u(t){var e="function"==typeof Map?new Map:void 0;return(u=function(t){if(null===t||(n=t,-1===Function.toString.call(n).indexOf("[native code]")))return t;var n;if("function"!=typeof t)throw new TypeError("Super expression must either be null or a function");if(void 0!==e){if(e.has(t))return e.get(t);e.set(t,r)}function r(){return a(t,arguments,s(this).constructor)}return r.prototype=Object.create(t.prototype,{constructor:{value:r,enumerable:!1,writable:!0,configurable:!0}}),f(r,t)})(t)}function a(t,e,n){return(a=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],function(){})),!0}catch(t){return!1}}()?Reflect.construct:function(t,e,n){var r=[null];r.push.apply(r,e);var o=new(Function.bind.apply(t,r));return n&&f(o,n.prototype),o}).apply(null,arguments)}function f(t,e){return(f=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t})(t,e)}function s(t){return(s=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}var l=function(t){function e(){return function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,e),c(this,s(e).apply(this,arguments))}var n,o,a;return function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&f(t,e)}(e,u(HTMLElement)),n=e,(o=[{key:"_onClick",value:function(){Object(r.a)(this,"hass-more-info",{entityId:this.config.entity})}},{key:"setConfig",value:function(t){if(!t.entity)throw new Error("You need to define an entity");this.config=t}},{key:"getCardSize",value:function(){return 3}},{key:"hass",set:function(t){if(!this.content){var e=document.createElement("ha-card");this.content=document.createElement("div"),e.appendChild(this.content),e.style="background: none;",this.appendChild(e),this.addEventListener("click",function(){this._onClick()})}var n=this.config.off_image,r=this.config.entity,o=t.states[r],i=o?o.state:"unavailable",c=this.config.class||this.config.entity.replace(".","_");if(this.setAttribute("class",c),o){var u=o.attributes.entity_picture;this.content.innerHTML="playing"===i&&u?'<img src="'.concat(u,'" width=100% height=100%" style="">'):n?'<img src="'.concat(n,'" width=100% align="center" style="">'):'<img src="/static/icons/tile-win-310x150.png" width=100% align="center" style="">'}else this.content.innerHTML='<img src="/static/icons/tile-win-310x150.png" width=100% align="center" style="">'}}])&&i(n.prototype,o),a&&i(n,a),e}();customElements.define("hui-ais-now-playing-poster-card",l)}}]);
//# sourceMappingURL=chunk.63576e3c2962a3c3eaa1.js.map