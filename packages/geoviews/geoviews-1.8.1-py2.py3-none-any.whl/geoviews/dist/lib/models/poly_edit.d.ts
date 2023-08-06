import * as p from "@bokehjs/core/properties";
import { GestureEvent, UIEvent, TapEvent } from "@bokehjs/core/ui_events";
import { GlyphRenderer } from "@bokehjs/models/renderers/glyph_renderer";
import { HasXYGlyph } from "@bokehjs/models/tools/edit/edit_tool";
import { PolyEditTool, PolyEditToolView } from "@bokehjs/models/tools/edit/poly_edit_tool";
export declare class PolyVertexEditToolView extends PolyEditToolView {
    model: PolyVertexEditTool;
    deactivate(): void;
    _pan(ev: GestureEvent): void;
    _pan_end(ev: GestureEvent): void;
    _drag_points(ev: UIEvent, renderers: (GlyphRenderer & HasXYGlyph)[]): number[][];
    _set_vertices(xs: number[] | number, ys: number[] | number, styles?: any): void;
    _move_linked(points: number[][]): void;
    _tap(ev: TapEvent): void;
    _show_vertices(ev: UIEvent): void;
}
export declare namespace PolyVertexEditTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = PolyEditTool.Props & {
        end_style: p.Property<any>;
        node_style: p.Property<any>;
    };
}
export interface PolyVertexEditTool extends PolyEditTool.Attrs {
}
export declare class PolyVertexEditTool extends PolyEditTool {
    properties: PolyVertexEditTool.Props;
    constructor(attrs?: Partial<PolyVertexEditTool.Attrs>);
    static __module__: string;
    static init_PolyVertexEditTool(): void;
}
