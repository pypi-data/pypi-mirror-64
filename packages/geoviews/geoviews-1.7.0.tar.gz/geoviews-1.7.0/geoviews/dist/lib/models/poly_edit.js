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
var poly_edit_tool_1 = require("@bokehjs/models/tools/edit/poly_edit_tool");
var PolyVertexEditToolView = /** @class */ (function (_super) {
    __extends(PolyVertexEditToolView, _super);
    function PolyVertexEditToolView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PolyVertexEditToolView.prototype.deactivate = function () {
        this._hide_vertices();
        if (!this._selected_renderer) {
            return;
        }
        else if (this._drawing) {
            this._remove_vertex();
            this._drawing = false;
        }
        this._emit_cds_changes(this._selected_renderer.data_source, false, true, false);
    };
    PolyVertexEditToolView.prototype._pan = function (ev) {
        if (this._basepoint == null)
            return;
        var points = this._drag_points(ev, [this.model.vertex_renderer]);
        if (!ev.shiftKey) {
            this._move_linked(points);
        }
        if (this._selected_renderer)
            this._selected_renderer.data_source.change.emit();
    };
    PolyVertexEditToolView.prototype._pan_end = function (ev) {
        if (this._basepoint == null)
            return;
        var points = this._drag_points(ev, [this.model.vertex_renderer]);
        if (!ev.shiftKey) {
            this._move_linked(points);
        }
        this._emit_cds_changes(this.model.vertex_renderer.data_source, false, true, true);
        if (this._selected_renderer) {
            this._emit_cds_changes(this._selected_renderer.data_source);
        }
        this._basepoint = null;
    };
    PolyVertexEditToolView.prototype._drag_points = function (ev, renderers) {
        if (this._basepoint == null)
            return [];
        var _a = this._basepoint, bx = _a[0], by = _a[1];
        var points = [];
        for (var _i = 0, renderers_1 = renderers; _i < renderers_1.length; _i++) {
            var renderer = renderers_1[_i];
            var basepoint = this._map_drag(bx, by, renderer);
            var point = this._map_drag(ev.sx, ev.sy, renderer);
            if (point == null || basepoint == null) {
                continue;
            }
            var x = point[0], y = point[1];
            var px = basepoint[0], py = basepoint[1];
            var _b = [x - px, y - py], dx = _b[0], dy = _b[1];
            // Type once dataspecs are typed
            var glyph = renderer.glyph;
            var cds = renderer.data_source;
            var _c = [glyph.x.field, glyph.y.field], xkey = _c[0], ykey = _c[1];
            for (var _d = 0, _e = cds.selected.indices; _d < _e.length; _d++) {
                var index = _e[_d];
                var point_1 = [];
                if (xkey) {
                    point_1.push(cds.data[xkey][index]);
                    cds.data[xkey][index] += dx;
                }
                if (ykey) {
                    point_1.push(cds.data[ykey][index]);
                    cds.data[ykey][index] += dy;
                }
                point_1.push(dx);
                point_1.push(dy);
                points.push(point_1);
            }
            cds.change.emit();
        }
        this._basepoint = [ev.sx, ev.sy];
        return points;
    };
    PolyVertexEditToolView.prototype._set_vertices = function (xs, ys, styles) {
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
    PolyVertexEditToolView.prototype._move_linked = function (points) {
        if (!this._selected_renderer)
            return;
        var renderer = this._selected_renderer;
        var glyph = renderer.glyph;
        var cds = renderer.data_source;
        var _a = [glyph.xs.field, glyph.ys.field], xkey = _a[0], ykey = _a[1];
        var xpaths = cds.data[xkey];
        var ypaths = cds.data[ykey];
        for (var _i = 0, points_1 = points; _i < points_1.length; _i++) {
            var point = points_1[_i];
            var x = point[0], y = point[1], dx = point[2], dy = point[3];
            for (var index = 0; index < xpaths.length; index++) {
                var xs = xpaths[index];
                var ys = ypaths[index];
                for (var i = 0; i < xs.length; i++) {
                    if ((xs[i] == x) && (ys[i] == y)) {
                        xs[i] += dx;
                        ys[i] += dy;
                    }
                }
            }
        }
    };
    PolyVertexEditToolView.prototype._tap = function (ev) {
        var _a;
        var renderer = this.model.vertex_renderer;
        var point = this._map_drag(ev.sx, ev.sy, renderer);
        if (point == null)
            return;
        else if (this._drawing && this._selected_renderer) {
            var x = point[0], y = point[1];
            var cds = renderer.data_source;
            // Type once dataspecs are typed
            var glyph = renderer.glyph;
            var _b = [glyph.x.field, glyph.y.field], xkey = _b[0], ykey = _b[1];
            var indices = cds.selected.indices;
            _a = this._snap_to_vertex(ev, x, y), x = _a[0], y = _a[1];
            var index = indices[0];
            cds.selected.indices = [index + 1];
            if (xkey) {
                var xs = cds.get_array(xkey);
                var nx = xs[index];
                xs[index] = x;
                xs.splice(index + 1, 0, nx);
            }
            if (ykey) {
                var ys = cds.get_array(ykey);
                var ny = ys[index];
                ys[index] = y;
                ys.splice(index + 1, 0, ny);
            }
            cds.change.emit();
            this._emit_cds_changes(this._selected_renderer.data_source, true, false, true);
            return;
        }
        var append = ev.shiftKey;
        this._select_event(ev, append, [renderer]);
    };
    PolyVertexEditToolView.prototype._show_vertices = function (ev) {
        if (!this.model.active)
            return;
        var renderers = this._select_event(ev, false, this.model.renderers);
        if (!renderers.length) {
            this._hide_vertices();
            this._selected_renderer = null;
            this._drawing = false;
            return;
        }
        var renderer = renderers[0];
        var glyph = renderer.glyph;
        var cds = renderer.data_source;
        var index = cds.selected.indices[0];
        var _a = [glyph.xs.field, glyph.ys.field], xkey = _a[0], ykey = _a[1];
        var xs;
        var ys;
        if (xkey) {
            xs = cds.data[xkey][index];
            if (!types_1.isArray(xs))
                cds.data[xkey][index] = xs = Array.from(xs);
        }
        else {
            xs = glyph.xs.value;
        }
        if (ykey) {
            ys = cds.data[ykey][index];
            if (!types_1.isArray(ys))
                cds.data[ykey][index] = ys = Array.from(ys);
        }
        else {
            ys = glyph.ys.value;
        }
        var styles = {};
        for (var _i = 0, _b = object_1.keys(this.model.end_style); _i < _b.length; _i++) {
            var key = _b[_i];
            styles[key] = [this.model.end_style[key]];
        }
        for (var _c = 0, _d = object_1.keys(this.model.node_style); _c < _d.length; _c++) {
            var key = _d[_c];
            for (var index_1 = 0; index_1 < (xs.length - 2); index_1++) {
                styles[key].push(this.model.node_style[key]);
            }
        }
        for (var _e = 0, _f = object_1.keys(this.model.end_style); _e < _f.length; _e++) {
            var key = _f[_e];
            styles[key].push(this.model.end_style[key]);
        }
        this._selected_renderer = renderer;
        this._set_vertices(xs, ys, styles);
    };
    PolyVertexEditToolView.__name__ = "PolyVertexEditToolView";
    return PolyVertexEditToolView;
}(poly_edit_tool_1.PolyEditToolView));
exports.PolyVertexEditToolView = PolyVertexEditToolView;
var PolyVertexEditTool = /** @class */ (function (_super) {
    __extends(PolyVertexEditTool, _super);
    function PolyVertexEditTool(attrs) {
        return _super.call(this, attrs) || this;
    }
    PolyVertexEditTool.init_PolyVertexEditTool = function () {
        this.prototype.default_view = PolyVertexEditToolView;
        this.define({
            node_style: [p.Any, {}],
            end_style: [p.Any, {}],
        });
    };
    PolyVertexEditTool.__name__ = "PolyVertexEditTool";
    PolyVertexEditTool.__module__ = "geoviews.models.custom_tools";
    return PolyVertexEditTool;
}(poly_edit_tool_1.PolyEditTool));
exports.PolyVertexEditTool = PolyVertexEditTool;
PolyVertexEditTool.init_PolyVertexEditTool();
//# sourceMappingURL=poly_edit.js.map