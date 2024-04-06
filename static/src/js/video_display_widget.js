/** @odoo-module */

import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { CharField, charField} from "@web/views/fields/char/char_field";
import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class VideoDisplayWidget extends Component {

    /**
    * @param {char} newValue
    */
    onChange(newValue) {
        this.props.update(newValue);
    }
}

VideoDisplayWidget.template =xml`
<templates>
    <t>
        <div>
            <video width="640" height="360" controls>
                <source src=""https://www.bing.com/ck/a?!&&p=9028fff980540773JmltdHM9MTcxMjM2MTYwMCZpZ3VpZD0wMDI4MzI1ZC01YzhlLTZiNDYtMjExYi0yMDljNWRmMjZhYjEmaW5zaWQ9NTQ4Ng&ptn=3&ver=2&hsh=3&fclid=0028325d-5c8e-6b46-211b-209c5df26ab1&u=a1L3ZpZGVvcy9yaXZlcnZpZXcvcmVsYXRlZHZpZGVvP3E9bWVudGlvbitzdGF0aWMrZm9sZGVyK2luK09kb28rMTcrY29uZitvcittYW5pZmVzdCZtaWQ9MTBENDIwMzNFQjdFQThGQ0RBQUQxMEQ0MjAzM0VCN0VBOEZDREFBRCZGT1JNPVZJUkU&ntb=1"" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <p> lalaalalalalalalalal </p>
        </div>
    </t>
</templates>
`;
VideoDisplayWidget.props = {
    ...standardFieldProps,
};

export const videoDisplayWidget = {
    ...charField,
    component: VideoDisplayWidget,
};
// VideoDisplayWidget.supportedTypes = ["Char"];

registry.category("fields").add("video_display", videoDisplayWidget);
