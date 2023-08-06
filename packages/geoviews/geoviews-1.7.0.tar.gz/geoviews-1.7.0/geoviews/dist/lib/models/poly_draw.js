"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var p = require("@bokehjs/core/properties");
var object_1 = require("@bokehjs/core/util/object");
var types_1 = require("@bokehjs/core/util/types");
var poly_draw_tool_1 = require("@bokehjs/models/tools/edit/poly_draw_tool");
var PolyVertexDrawToolView = /** @class */ (function (_super) {
    __extends(PolyVertexDrawToolView, _super);
    function PolyVertexDrawToolView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PolyVertexDrawToolView.prototype._split_path = function (x, y) {
        for (var r = 0; r < this.model.renderers.length; r++) {
            var renderer = this.model.renderers[r];
            var glyph = renderer.glyph;
            var cds = renderer.data_source;
            var _a = [glyph.xs.field, glyph.ys.field], xkey = _a[0], ykey = _a[1];
            var xpaths = cds.data[xkey];
            var ypaths = cds.data[ykey];
            for (var index = 0; index < xpaths.length; index++) {
                var xs = xpaths[index];
                if (!types_1.isArray(xs)) {
                    xs = Array.from(xs);
                    cds.data[xkey][index] = xs;
                }
                var ys = ypaths[index];
                if (!types_1.isArray(ys)) {
                    ys = Array.from(ys);
                    cds.data[ykey][index] = ys;
                }
                for (var i = 0; i < xs.length; i++) {
                    if ((xs[i] == x) && (ys[i] == y) && (i != 0) && (i != (xs.length - 1))) {
                        xpaths.splice(index + 1, 0, xs.slice(i));
                        ypaths.splice(index + 1, 0, ys.slice(i));
                        xs.splice(i + 1);
                        ys.splice(i + 1);
                        for (var _i = 0, _b = cds.columns(); _i < _b.length; _i++) {
                            var column = _b[_i];
                            if ((column !== xkey) && (column != ykey))
                                cds.data[column].splice(index + 1, 0, cds.data[column][index]);
                        }
                        return;
                    }
                }
            }
        }
    };
    PolyVertexDrawToolView.prototype._snap_to_vertex = function (ev, x, y) {
        if (this.model.vertex_renderer) {
            // If an existing vertex is hit snap to it
            var vertex_selected = this._select_event(ev, false, [this.model.vertex_renderer]);
            var point_ds = this.model.vertex_renderer.data_source;
            // Type once dataspecs are typed
            var point_glyph = this.model.vertex_renderer.glyph;
            var _a = [point_glyph.x.field, point_glyph.y.field], pxkey = _a[0], pykey = _a[1];
            if (vertex_selected.length) {
                // If existing vertex is hit split path at that location
                // converting to feature vertex
                var index = point_ds.selected.indices[0];
                if (pxkey)
                    x = point_ds.data[pxkey][index];
                if (pykey)
                    y = point_ds.data[pykey][index];
                if (ev.type != 'mousemove')
                    this._split_path(x, y);
                point_ds.selection_manager.clear();
            }
        }
        return [x, y];
    };
    PolyVertexDrawToolView.prototype._set_vertices = function (xs, ys, styles) {
        var point_glyph = this.model.vertex_renderer.glyph;
        var point_cds = this.model.vertex_renderer.data_source;
        var _a = [point_glyph.x.field, point_glyph.y.field], pxkey = _a[0], pykey = _a[1];
        if (pxkey) {
            if (types_1.isArray(xs))
                point_cds.data[pxkey] = xs;
            else
                point_glyph.x = { value: xs };
        }
        if (pykey) {
            if (types_1.isArray(ys))
                point_cds.data[pykey] = ys;
            else
                point_glyph.y = { value: ys };
        }
        if (styles != null) {
            for (var _i = 0, _b = object_1.keys(styles); _i < _b.length; _i++) {
                var key = _b[_i];
                point_cds.data[key] = styles[key];
                point_glyph[key] = { field: key };
            }
        }
        else {
            for (var _c = 0, _d = point_cds.columns(); _c < _d.length; _c++) {
                var col = _d[_c];
                point_cds.data[col] = [];
            }
        }
        this._emit_cds_changes(point_cds, true, true, false);
    };
    PolyVertexDrawToolView.prototype._show_vertices = function () {
        if (!this.model.active) {
            return;
        }
        var xs = [];
        var ys = [];
        var styles = {};
        for (var _i = 0, _a = object_1.keys(this.model.end_style); _i < _a.length; _i++) {
            var key = _a[_i];
            styles[key] = [];
        }
        for (var i = 0; i < this.model.renderers.length; i++) {
            var renderer = this.model.renderers[i];
            var cds = renderer.data_source;
            var glyph = renderer.glyph;
            var _b = [glyph.xs.field, glyph.ys.field], xkey = _b[0], ykey = _b[1];
            for (var _c = 0, _d = cds.get_array(xkey); _c < _d.length; _c++) {
                var array = _d[_c];
                Array.prototype.push.apply(xs, array);
                for (var _e = 0, _f = object_1.keys(this.model.end_style); _e < _f.length; _e++) {
                    var key = _f[_e];
                    styles[key].push(this.model.end_style[key]);
                }
                for (var _g = 0, _h = object_1.keys(this.model.node_style); _g < _h.length; _g++) {
                    var key = _h[_g];
                    for (var index = 0; index < (array.length - 2); index++) {
                        styles[key].push(this.model.node_style[key]);
                    }
                }
                for (var _j = 0, _k = object_1.keys(this.model.end_style); _j < _k.length; _j++) {
                    var key = _k[_j];
                    styles[key].push(this.model.end_style[key]);
                }
            }
            for (var _l = 0, _m = cds.get_array(ykey); _l < _m.length; _l++) {
                var array = _m[_l];
                Array.prototype.push.apply(ys, array);
            }
            if (this._drawing && (i == (this.model.renderers.length - 1))) {
                // Skip currently drawn vertex
                xs.splice(xs.length - 1, 1);
                ys.splice(ys.length - 1, 1);
                for (var _o = 0, _p = object_1.keys(styles); _o < _p.length; _o++) {
                    var key = _p[_o];
                    styles[key].splice(styles[key].length - 1, 1);
                }
            }
        }
        this._set_vertices(xs, ys, styles);
    };
    PolyVertexDrawToolView.prototype._remove = function () {
        var renderer = this.model.renderers[0];
        var cds = renderer.data_source;
        var glyph = renderer.glyph;
        var _a = [glyph.xs.field, glyph.ys.field], xkey = _a[0], ykey = _a[1];
        if (xkey) {
            var xidx = cds.data[xkey].length - 1;
            var xs = cds.get_array(xkey)[xidx];
            xs.splice(xs.length - 1, 1);
            if (xs.length == 1)
                cds.data[xkey].splice(xidx, 1);
        }
        if (ykey) {
            var yidx = cds.data[ykey].length - 1;
            var ys = cds.get_array(ykey)[yidx];
            ys.splice(ys.length - 1, 1);
            if (ys.length == 1)
                cds.data[ykey].splice(yidx, 1);
        }
        this._emit_cds_changes(cds);
        this._drawing = false;
        this._show_vertices();
    };
    PolyVertexDrawToolView.__name__ = "PolyVertexDrawToolView";
    return PolyVertexDrawToolView;
}(poly_draw_tool_1.PolyDrawToolView));
exports.PolyVertexDrawToolView = PolyVertexDrawToolView;
var PolyVertexDrawTool = /** @class */ (function (_super) {
    __extends(PolyVertexDrawTool, _super);
    function PolyVertexDrawTool(attrs) {
        return _super.call(this, attrs) || this;
    }
    PolyVertexDrawTool.init_PolyVertexDrawTool = function () {
        this.prototype.default_view = PolyVertexDrawToolView;
        this.define({
            end_style: [p.Any, {}],
            node_style: [p.Any, {}],
        });
    };
    PolyVertexDrawTool.__name__ = "PolyVertexDrawTool";
    PolyVertexDrawTool.__module__ = "geoviews.models.custom_tools";
    return PolyVertexDrawTool;
}(poly_draw_tool_1.PolyDrawTool));
exports.PolyVertexDrawTool = PolyVertexDrawTool;
PolyVertexDrawTool.init_PolyVertexDrawTool();
//# sourceMappingURL=poly_draw.js.map