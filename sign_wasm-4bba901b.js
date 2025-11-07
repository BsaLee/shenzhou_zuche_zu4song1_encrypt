let L, $, O, R, z;
let __tla = (async () => {
  const h = "https://fes.zuchecdn.com/cdn/h/vd/zuche/carfes/taishan/components/1.2.7/assets/sign_wasm_bg-b8af3646.wasm", T = async (e = {}, _) => {
    let c;
    if (_.startsWith("data:")) {
      const r = _.replace(/^data:.*?base64,/, "");
      let t;
      if (typeof Buffer == "function" && typeof Buffer.from == "function")
        t = Buffer.from(r, "base64");
      else if (typeof atob == "function") {
        const i = atob(r);
        t = new Uint8Array(i.length);
        for (let o = 0; o < i.length; o++)
          t[o] = i.charCodeAt(o);
      } else
        throw new Error("Cannot decode base64-encoded data URL");
      c = await WebAssembly.instantiate(t, e);
    } else {
      const r = await fetch(_), t = r.headers.get("Content-Type") || "";
      if ("instantiateStreaming" in WebAssembly && t.startsWith("application/wasm"))
        c = await WebAssembly.instantiateStreaming(r, e);
      else {
        const i = await r.arrayBuffer();
        c = await WebAssembly.instantiate(i, e);
      }
    }
    return c.instance.exports;
  };
  URL = globalThis.URL;
  const a = await T({}, h), v = a.memory, x = a.decrypt, k = a.encrypt, A = a.md5, W = a.sign, S = a.__wbindgen_add_to_stack_pointer, E = a.__wbindgen_malloc, M = a.__wbindgen_realloc, U = a.__wbindgen_free, C = Object.freeze(Object.defineProperty({
    __proto__: null,
    __wbindgen_add_to_stack_pointer: S,
    __wbindgen_free: U,
    __wbindgen_malloc: E,
    __wbindgen_realloc: M,
    decrypt: x,
    encrypt: k,
    md5: A,
    memory: v,
    sign: W
  }, Symbol.toStringTag, {
    value: "Module"
  }));
  let n;
  L = function(e) {
    n = e;
  };
  let l = 0, u = null;
  function g() {
    return (u === null || u.byteLength === 0) && (u = new Uint8Array(n.memory.buffer)), u;
  }
  const B = typeof TextEncoder > "u" ? (0, module.require)("util").TextEncoder : TextEncoder;
  let w = new B("utf-8");
  const D = typeof w.encodeInto == "function" ? function(e, _) {
    return w.encodeInto(e, _);
  } : function(e, _) {
    const c = w.encode(e);
    return _.set(c), {
      read: e.length,
      written: c.length
    };
  };
  function y(e, _, c) {
    if (c === void 0) {
      const d = w.encode(e), f = _(d.length, 1) >>> 0;
      return g().subarray(f, f + d.length).set(d), l = d.length, f;
    }
    let r = e.length, t = _(r, 1) >>> 0;
    const i = g();
    let o = 0;
    for (; o < r; o++) {
      const d = e.charCodeAt(o);
      if (d > 127)
        break;
      i[t + o] = d;
    }
    if (o !== r) {
      o !== 0 && (e = e.slice(o)), t = c(t, r, r = o + e.length * 3, 1) >>> 0;
      const d = g().subarray(t + o, t + r), f = D(e, d);
      o += f.written, t = c(t, r, o, 1) >>> 0;
    }
    return l = o, t;
  }
  let b = null;
  function s() {
    return (b === null || b.byteLength === 0) && (b = new Int32Array(n.memory.buffer)), b;
  }
  const I = typeof TextDecoder > "u" ? (0, module.require)("util").TextDecoder : TextDecoder;
  let p = new I("utf-8", {
    ignoreBOM: true,
    fatal: true
  });
  p.decode();
  function m(e, _) {
    return e = e >>> 0, p.decode(g().subarray(e, e + _));
  }
  $ = function(e) {
    let _, c;
    try {
      const i = n.__wbindgen_add_to_stack_pointer(-16), o = y(e, n.__wbindgen_malloc, n.__wbindgen_realloc), d = l;
      n.decrypt(i, o, d);
      var r = s()[i / 4 + 0], t = s()[i / 4 + 1];
      return _ = r, c = t, m(r, t);
    } finally {
      n.__wbindgen_add_to_stack_pointer(16), n.__wbindgen_free(_, c, 1);
    }
  };
  O = function(e) {
    let _, c;
    try {
      const i = n.__wbindgen_add_to_stack_pointer(-16), o = y(e, n.__wbindgen_malloc, n.__wbindgen_realloc), d = l;
      n.encrypt(i, o, d);
      var r = s()[i / 4 + 0], t = s()[i / 4 + 1];
      return _ = r, c = t, m(r, t);
    } finally {
      n.__wbindgen_add_to_stack_pointer(16), n.__wbindgen_free(_, c, 1);
    }
  };
  R = function(e) {
    let _, c;
    try {
      const i = n.__wbindgen_add_to_stack_pointer(-16), o = y(e, n.__wbindgen_malloc, n.__wbindgen_realloc), d = l;
      n.md5(i, o, d);
      var r = s()[i / 4 + 0], t = s()[i / 4 + 1];
      return _ = r, c = t, m(r, t);
    } finally {
      n.__wbindgen_add_to_stack_pointer(16), n.__wbindgen_free(_, c, 1);
    }
  };
  z = function(e) {
    let _, c;
    try {
      const i = n.__wbindgen_add_to_stack_pointer(-16), o = y(e, n.__wbindgen_malloc, n.__wbindgen_realloc), d = l;
      n.sign(i, o, d);
      var r = s()[i / 4 + 0], t = s()[i / 4 + 1];
      return _ = r, c = t, m(r, t);
    } finally {
      n.__wbindgen_add_to_stack_pointer(16), n.__wbindgen_free(_, c, 1);
    }
  };
  L(C);
})();
export {
  __tla,
  L as __wbg_set_wasm,
  $ as decrypt,
  O as encrypt,
  R as md5,
  z as sign
};
