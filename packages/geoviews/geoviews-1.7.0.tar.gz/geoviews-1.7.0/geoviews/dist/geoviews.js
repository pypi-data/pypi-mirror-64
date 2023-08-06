/*!
 * Copyright (c) 2012 - 2019, Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
*/
(function(root, factory) {
  factory(root["Bokeh"]);
})(this, function(Bokeh) {
  var define;
  return (function(modules, entry, aliases, externals) {
    if (Bokeh != null) {
      return Bokeh.register_plugin(modules, entry, aliases, externals);
    } else {
      throw new Error("Cannot find Bokeh. You have to load it prior to loading plugins.");
    }
  })
({
"38f4b8800f": /* index.js */ function _(require, module, exports) {
    var GeoViews = require("b9b392174d") /* ./models */;
    exports.GeoViews = GeoViews;
    var base_1 = require("@bokehjs/base");
    base_1.register_models(GeoViews);
},
"b9b392174d": /* models/index.js */ function _(require, module, exports) {
    var checkpoint_tool_1 = require("27f5421c63") /* ./checkpoint_tool */;
    exports.CheckpointTool = checkpoint_tool_1.CheckpointTool;
    var clear_tool_1 = require("65e2b641a2") /* ./clear_tool */;
    exports.ClearTool = clear_tool_1.ClearTool;
    var poly_draw_1 = require("bf8d72a956") /* ./poly_draw */;
    exports.PolyVertexDrawTool = poly_draw_1.PolyVertexDrawTool;
    var poly_edit_1 = require("548fd712fd") /* ./poly_edit */;
    exports.PolyVertexEditTool = poly_edit_1.PolyVertexEditTool;
    var restore_tool_1 = require("f3e27c114e") /* ./restore_tool */;
    exports.RestoreTool = restore_tool_1.RestoreTool;
},
"27f5421c63": /* models/checkpoint_tool.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var array_1 = require("@bokehjs/core/util/array");
    var action_tool_1 = require("@bokehjs/models/tools/actions/action_tool");
    var CheckpointToolView = /** @class */ (function (_super) {
        __extends(CheckpointToolView, _super);
        function CheckpointToolView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        CheckpointToolView.prototype.doit = function () {
            var sources = this.model.sources;
            for (var _i = 0, sources_1 = sources; _i < sources_1.length; _i++) {
                var source = sources_1[_i];
                if (!source.buffer) {
                    source.buffer = [];
                }
                var data_copy = {};
                for (var key in source.data) {
                    var column = source.data[key];
                    var new_column = [];
                    for (var _a = 0, column_1 = column; _a < column_1.length; _a++) {
                        var arr = column_1[_a];
                        if (Array.isArray(arr) || (ArrayBuffer.isView(arr))) {
                            new_column.push(array_1.copy(arr));
                        }
                        else {
                            new_column.push(arr);
                        }
                    }
                    data_copy[key] = new_column;
                }
                source.buffer.push(data_copy);
            }
        };
        CheckpointToolView.__name__ = "CheckpointToolView";
        return CheckpointToolView;
    }(action_tool_1.ActionToolView));
    exports.CheckpointToolView = CheckpointToolView;
    var CheckpointTool = /** @class */ (function (_super) {
        __extends(CheckpointTool, _super);
        function CheckpointTool(attrs) {
            var _this = _super.call(this, attrs) || this;
            _this.tool_name = "Checkpoint";
            _this.icon = "bk-tool-icon-save";
            return _this;
        }
        CheckpointTool.init_CheckpointTool = function () {
            this.prototype.default_view = CheckpointToolView;
            this.define({
                sources: [p.Array, []],
            });
        };
        CheckpointTool.__name__ = "CheckpointTool";
        CheckpointTool.__module__ = "geoviews.models.custom_tools";
        return CheckpointTool;
    }(action_tool_1.ActionTool));
    exports.CheckpointTool = CheckpointTool;
    CheckpointTool.init_CheckpointTool();
},
"65e2b641a2": /* models/clear_tool.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var action_tool_1 = require("@bokehjs/models/tools/actions/action_tool");
    var ClearToolView = /** @class */ (function (_super) {
        __extends(ClearToolView, _super);
        function ClearToolView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        ClearToolView.prototype.doit = function () {
            for (var _i = 0, _a = this.model.sources; _i < _a.length; _i++) {
                var source = _a[_i];
                for (var column in source.data) {
                    source.data[column] = [];
                }
                source.change.emit();
                source.properties.data.change.emit();
            }
        };
        ClearToolView.__name__ = "ClearToolView";
        return ClearToolView;
    }(action_tool_1.ActionToolView));
    exports.ClearToolView = ClearToolView;
    var ClearTool = /** @class */ (function (_super) {
        __extends(ClearTool, _super);
        function ClearTool(attrs) {
            var _this = _super.call(this, attrs) || this;
            _this.tool_name = "Clear data";
            _this.icon = "bk-tool-icon-reset";
            return _this;
        }
        ClearTool.init_ClearTool = function () {
            this.prototype.type = "ClearTool";
            this.prototype.default_view = ClearToolView;
            this.define({
                sources: [p.Array, []],
            });
        };
        ClearTool.__name__ = "ClearTool";
        ClearTool.__module__ = "geoviews.models.custom_tools";
        return ClearTool;
    }(action_tool_1.ActionTool));
    exports.ClearTool = ClearTool;
    ClearTool.init_ClearTool();
},
"bf8d72a956": /* models/poly_draw.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
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
},
"548fd712fd": /* models/poly_edit.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
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
},
"f3e27c114e": /* models/restore_tool.js */ function _(require, module, exports) {
    var __extends = (this && this.__extends) || (function () {
        var extendStatics = function (d, b) {
            extendStatics = Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
                function (d, b) { for (var p in b)
                    if (b.hasOwnProperty(p))
                        d[p] = b[p]; };
            return extendStatics(d, b);
        };
        return function (d, b) {
            extendStatics(d, b);
            function __() { this.constructor = d; }
            d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
        };
    })();
    var p = require("@bokehjs/core/properties");
    var action_tool_1 = require("@bokehjs/models/tools/actions/action_tool");
    var RestoreToolView = /** @class */ (function (_super) {
        __extends(RestoreToolView, _super);
        function RestoreToolView() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        RestoreToolView.prototype.doit = function () {
            var sources = this.model.sources;
            for (var _i = 0, sources_1 = sources; _i < sources_1.length; _i++) {
                var source = sources_1[_i];
                if (!source.buffer || (source.buffer.length == 0)) {
                    continue;
                }
                source.data = source.buffer.pop();
                source.change.emit();
                source.properties.data.change.emit();
            }
        };
        RestoreToolView.__name__ = "RestoreToolView";
        return RestoreToolView;
    }(action_tool_1.ActionToolView));
    exports.RestoreToolView = RestoreToolView;
    var RestoreTool = /** @class */ (function (_super) {
        __extends(RestoreTool, _super);
        function RestoreTool(attrs) {
            var _this = _super.call(this, attrs) || this;
            _this.tool_name = "Restore";
            _this.icon = "bk-tool-icon-undo";
            return _this;
        }
        RestoreTool.init_RestoreTool = function () {
            this.prototype.default_view = RestoreToolView;
            this.define({
                sources: [p.Array, []]
            });
        };
        RestoreTool.__name__ = "RestoreTool";
        RestoreTool.__module__ = "geoviews.models.custom_tools";
        return RestoreTool;
    }(action_tool_1.ActionTool));
    exports.RestoreTool = RestoreTool;
    RestoreTool.init_RestoreTool();
},
}, "38f4b8800f", {"index":"38f4b8800f","models/index":"b9b392174d","models/checkpoint_tool":"27f5421c63","models/clear_tool":"65e2b641a2","models/poly_draw":"bf8d72a956","models/poly_edit":"548fd712fd","models/restore_tool":"f3e27c114e"}, {});
})

//# sourceMappingURL=geoviews.js.map
