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
//# sourceMappingURL=checkpoint_tool.js.map