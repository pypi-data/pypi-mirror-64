(self.webpackJsonp=self.webpackJsonp||[]).push([[55],{212:function(e,t,r){"use strict";r(211);var n=r(79),o=r(1),i=r(141),a={getTabbableNodes:function(e){var t=[];return this._collectTabbableNodes(e,t)?i.a._sortByTabIndex(t):t},_collectTabbableNodes:function(e,t){if(e.nodeType!==Node.ELEMENT_NODE||!i.a._isVisible(e))return!1;var r,n=e,a=i.a._normalizedTabIndex(n),l=a>0;a>=0&&t.push(n),r="content"===n.localName||"slot"===n.localName?Object(o.a)(n).getDistributedNodes():Object(o.a)(n.shadowRoot||n.root||n).children;for(var s=0;s<r.length;s++)l=this._collectTabbableNodes(r[s],t)||l;return l}};function l(e){return(l="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function s(e,t){return!t||"object"!==l(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function c(e){return(c=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function p(e,t){return(p=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}var u=customElements.get("paper-dialog"),d={get _focusableNodes(){return a.getTabbableNodes(this)}},f=function(e){function t(){return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t),s(this,c(t).apply(this,arguments))}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&p(e,t)}(t,Object(n["b"])([d],u)),t}();customElements.define("ha-paper-dialog",f)},882:function(e,t,r){"use strict";r.r(t),r.d(t,"HaDialogAisgalery",function(){return E});r(120),r(119),r(212),r(801);var n=r(71),o=r(0),i=r(44);function a(e){return(a="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function l(){var e=u(['\n      <style>\n        paper-dialog-scrollable {\n          --paper-dialog-scrollable: {\n            -webkit-overflow-scrolling: auto;\n            max-height: 50vh !important;\n          }\n        }\n\n        paper-dialog-scrollable.can-scroll {\n          --paper-dialog-scrollable: {\n            -webkit-overflow-scrolling: touch;\n            max-height: 50vh !important;\n          }\n        }\n\n        @media all and (max-width: 450px), all and (max-height: 500px) {\n          paper-dialog-scrollable {\n            --paper-dialog-scrollable: {\n              -webkit-overflow-scrolling: auto;\n              max-height: calc(100vh - 175px) !important;\n            }\n          }\n\n          paper-dialog-scrollable.can-scroll {\n            --paper-dialog-scrollable: {\n              -webkit-overflow-scrolling: touch;\n              max-height: calc(75vh - 175px) !important;\n            }\n          }\n        }\n        app-toolbar {\n          margin: 0;\n          padding: 0 16px;\n          color: var(--primary-text-color);\n          background-color: var(--secondary-background-color);\n        }\n        app-toolbar [main-title] {\n          margin-left: 16px;\n        }\n      </style>\n      <dom-module id="my-button" theme-for="vaadin-button">\n        <template>\n          <style>\n            :host {\n              color: var(--primary-color);\n              border: 1px solid;\n            }\n          </style>\n        </template>\n      </dom-module>\n      <ha-paper-dialog\n        with-backdrop\n        .opened=',"\n        @opened-changed=",'\n      >\n        <app-toolbar>\n          <paper-icon-button\n            icon="hass:close"\n            dialog-dismiss=""\n          ></paper-icon-button>\n          <div main-title="">Dodawanie zdjęć</div>\n        </app-toolbar>\n        <vaadin-upload\n          capture="camera"\n          accept="image/*"\n          noAuto="false"\n          style="text-align: center;"\n        >\n          <span slot="drop-label" style="color:white;"\n            >Możesz przeciągnąć i upuścić tu.</span\n          >\n        </vaadin-upload>\n      </ha-paper-dialog>\n    ']);return l=function(){return e},e}function s(e,t,r,n,o,i,a){try{var l=e[i](a),s=l.value}catch(c){return void r(c)}l.done?t(s):Promise.resolve(s).then(n,o)}function c(e){return function(){var t=this,r=arguments;return new Promise(function(n,o){var i=e.apply(t,r);function a(e){s(i,n,o,a,l,"next",e)}function l(e){s(i,n,o,a,l,"throw",e)}a(void 0)})}}function p(){var e=u(['\n        :host {\n          z-index: 103;\n        }\n\n        paper-icon-button {\n          color: var(--secondary-text-color);\n        }\n\n        paper-icon-button[active] {\n          color: var(--primary-color);\n        }\n\n        ha-paper-dialog {\n          width: 450px;\n          height: 350px;\n        }\n        a.button {\n          text-decoration: none;\n        }\n        a.button > mwc-button {\n          width: 100%;\n        }\n        .onboarding {\n          padding: 0 24px;\n        }\n        paper-dialog-scrollable.top-border::before {\n          content: "";\n          position: absolute;\n          top: 0;\n          left: 0;\n          right: 0;\n          height: 1px;\n          background: var(--divider-color);\n        }\n      ']);return p=function(){return e},e}function u(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function d(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function f(e,t){return(f=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function h(e){var t,r=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function y(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function g(e){var t=function(e,t){if("object"!==a(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==a(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===a(t)?t:String(t)}function w(e,t,r){return(w="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=k(e)););return e}(e,t);if(n){var o=Object.getOwnPropertyDescriptor(n,t);return o.get?o.get.call(r):o.value}})(e,t,r||e)}function k(e){return(k=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var E=function(e,t,r,n){var o=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(r){t.forEach(function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach(function(n){t.forEach(function(t){var o=t.placement;if(t.kind===n&&("static"===o||"prototype"===o)){var i="static"===o?e:r;this.defineClassElement(i,t)}},this)},this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],o={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,o)},this),e.forEach(function(e){if(!y(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)},this),!t)return{elements:r,finishers:n};var i=this.decorateConstructor(r,t);return n.push.apply(n,i.finishers),i.finishers=n,i},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],o=e.decorators,i=o.length-1;i>=0;i--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var l=this.fromElementDescriptor(e),s=this.toElementFinisherExtras((0,o[i])(l)||l);e=s.element,this.addElementPlacement(e,t),s.finisher&&n.push(s.finisher);var c=s.extras;if(c){for(var p=0;p<c.length;p++)this.addElementPlacement(c[p],t);r.push.apply(r,c)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var o=this.fromClassDescriptor(e),i=this.toClassDescriptor((0,t[n])(o)||o);if(void 0!==i.finisher&&r.push(i.finisher),void 0!==i.elements){e=i.elements;for(var a=0;a<e.length-1;a++)for(var l=a+1;l<e.length;l++)if(e[a].key===e[l].key&&e[a].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=g(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var i={kind:t,key:r,placement:n,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),i.initializer=e.initializer),i},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),r=v(e,"finisher"),n=this.toElementDescriptors(e.extras);return{element:t,finisher:r,extras:n}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=v(e,"finisher"),n=this.toElementDescriptors(e.elements);return{elements:n,finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}();if(n)for(var i=0;i<n.length;i++)o=n[i](o);var a=t(function(e){o.initializeInstanceElements(e,l.elements)},r),l=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===i.key&&e.placement===i.placement},n=0;n<e.length;n++){var o,i=e[n];if("method"===i.kind&&(o=t.find(r)))if(b(i.descriptor)||b(o.descriptor)){if(y(i)||y(o))throw new ReferenceError("Duplicated methods ("+i.key+") can't be decorated.");o.descriptor=i.descriptor}else{if(y(i)){if(y(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+i.key+").");o.decorators=i.decorators}m(i,o)}else t.push(i)}return t}(a.d.map(h)),e);return o.initializeClassElements(a.F,l.elements),o.runClassFinishers(a.F,l.finishers)}([Object(o.d)("ha-dialog-aisgalery")],function(e,t){var r=function(r){function n(){var t,r,o;return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,n),r=this,t=!(o=k(n).call(this))||"object"!==a(o)&&"function"!=typeof o?d(r):o,e(d(t)),t.loadVaadin(),t}return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&f(e,t)}(n,t),n}();return{F:r,d:[{kind:"get",static:!0,key:"styles",value:function(){return[i.c,Object(o.c)(p())]}},{kind:"field",decorators:[Object(o.g)()],key:"hass",value:void 0},{kind:"field",decorators:[Object(o.g)()],key:"_opened",value:function(){return!1}},{kind:"method",key:"showDialog",value:function(){var e=c(regeneratorRuntime.mark(function e(){return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:this._opened=!0,this.loadVaadin();case 2:case"end":return e.stop()}},e,this)}));return function(){return e.apply(this,arguments)}}()},{kind:"method",key:"render",value:function(){return Object(o.f)(l(),this._opened,this._openedChanged)}},{kind:"method",key:"loadVaadin",value:function(){var e=c(regeneratorRuntime.mark(function e(){var t=this;return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:customElements.whenDefined("vaadin-upload").then(c(regeneratorRuntime.mark(function e(){var r,o;return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:r=t.shadowRoot.querySelector("vaadin-upload"),o=Object(n.c)(),null!==r&&(r.set("i18n.addFiles.many","Wyślij zdjęcie [plik 5MB max] ..."),r.set("i18n.fileIsTooBig","Plik jest za duży. Maksymalnie można przesłać 5MB"),r.set("method","POST"),r.set("withCredentials",!0),r.set("target","api/ais_file/upload"),r.set("headers",{authorization:"Bearer "+o.access_token}),r.addEventListener("file-reject",function(e){console.log(e.detail.file.name+" error: "+e.detail.error)}));case 3:case"end":return e.stop()}},e)})));case 1:case"end":return e.stop()}},e)}));return function(){return e.apply(this,arguments)}}()},{kind:"method",key:"firstUpdated",value:function(e){w(k(r.prototype),"updated",this).call(this,e)}},{kind:"method",key:"updated",value:function(e){w(k(r.prototype),"updated",this).call(this,e)}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value,this.loadVaadin()}}]}},o.a)}}]);
//# sourceMappingURL=chunk.70bdbe00a26d41fe1dd2.js.map