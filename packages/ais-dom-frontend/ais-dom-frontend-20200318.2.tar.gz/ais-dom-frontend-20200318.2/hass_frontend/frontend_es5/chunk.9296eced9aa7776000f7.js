(self.webpackJsonp=self.webpackJsonp||[]).push([[144],{810:function(e,n,t){"use strict";t.r(n);t(162);var r=t(4),o=t(32);t(140),t(106);function a(e){return(a="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function l(){var e=function(e,n){n||(n=e.slice(0));return Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(n)}}))}(['\n      <style include="ha-style">\n        iframe {\n          border: 0;\n          width: 100%;\n          height: calc(100% - 64px);\n          background-color: var(--primary-background-color);\n        }\n      </style>\n      <app-toolbar>\n        <ha-menu-button hass="[[hass]]" narrow="[[narrow]]"></ha-menu-button>\n        <div main-title>[[panel.title]]</div>\n      </app-toolbar>\n\n      <iframe\n        src="[[panel.config.url]]"\n        sandbox="allow-forms allow-popups allow-pointer-lock allow-same-origin allow-scripts"\n        allowfullscreen="true"\n        webkitallowfullscreen="true"\n        mozallowfullscreen="true"\n      ></iframe>\n    ']);return l=function(){return e},e}function u(e,n){for(var t=0;t<n.length;t++){var r=n[t];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function i(e,n){return!n||"object"!==a(n)&&"function"!=typeof n?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):n}function c(e){return(c=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function f(e,n){return(f=Object.setPrototypeOf||function(e,n){return e.__proto__=n,e})(e,n)}var p=function(e){function n(){return function(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}(this,n),i(this,c(n).apply(this,arguments))}var t,a,p;return function(e,n){if("function"!=typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(n&&n.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),n&&f(e,n)}(n,o["a"]),t=n,p=[{key:"template",get:function(){return Object(r.a)(l())}},{key:"properties",get:function(){return{hass:Object,narrow:Boolean,panel:Object}}}],(a=null)&&u(t.prototype,a),p&&u(t,p),n}();customElements.define("ha-panel-iframe",p)}}]);
//# sourceMappingURL=chunk.9296eced9aa7776000f7.js.map