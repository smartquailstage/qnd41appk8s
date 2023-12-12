! function(a) {
    function i(a) {
        var b = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
        a = a.replace(b, function(a, b, c, d) {
            return b + b + c + c + d + d
        });
        var c = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(a);
        return c ? {
            r: parseInt(c[1], 16),
            g: parseInt(c[2], 16),
            b: parseInt(c[3], 16)
        } : null
    }

    function j() {
        return Math.floor(65536 * (1 + Math.random())).toString(16).substring(1)
    }

    function k() {
        return j() + j() + "-" + j() + "-" + j() + "-" + j() + "-" + j() + j() + j()
    }

    function l(a) {
        var b = a.match(/^[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{1,2}:[0-9]{2}:[0-9]{2}$/);
        if (null !== b && b.length > 0) {
            var c = a.split(" "),
                d = c[0].split("-"),
                e = c[1].split(":");
            return new Date(d[0], d[1] - 1, d[2], e[0], e[1], e[2])
        }
        var f = Date.parse(a);
        return isNaN(f) ? (f = Date.parse(a.replace(/-/g, "/").replace("T", " ")), isNaN(f) ? new Date : f) : f
    }

    function m(a, b, c, d, e) {
        var f = {},
            g = {},
            i = {},
            j = {},
            k = {},
            l = {},
            m = null;
        for (var n in d) {
            var p, o = d[n];
            p = null === m ? c / h[o] : h[m] / h[o];
            var q = a / h[o],
                r = b / h[o];
            e && (q = Math.floor(q)), e && (r = Math.floor(r)), "Days" !== o && (q %= p, r %= p), f[o] = q, i[o] = Math.abs(q), g[o] = r, l[o] = Math.abs(r), j[o] = Math.abs(q) / p, k[o] = Math.abs(r) / p, m = o
        }
        return {
            raw_time: f,
            raw_old_time: g,
            time: i,
            old_time: l,
            pct: j,
            old_pct: k
        }
    }
    var b = !1,
        c = 200,
        f = ("#debug" === location.hash, ["Days", "Hours", "Minutes", "Seconds"]),
        g = {
            Seconds: "Minutes",
            Minutes: "Hours",
            Hours: "Days",
            Days: "Years"
        },
        h = {
            Seconds: 1,
            Minutes: 60,
            Hours: 3600,
            Days: 86400,
            Months: 2678400,
            Years: 31536e3
        },
        n = {};
    window !== window.top && "undefined" != typeof window.top.TC_Instance_List ? n = window.top.TC_Instance_List : window.top.TC_Instance_List = n,
        function() {
            for (var a = ["webkit", "moz"], b = 0; b < a.length && !window.top.requestAnimationFrame; ++b) window.top.requestAnimationFrame = window.top[a[b] + "RequestAnimationFrame"], window.top.cancelAnimationFrame = window.top[a[b] + "CancelAnimationFrame"];
            window.top.requestAnimationFrame && window.top.cancelAnimationFrame || (window.top.requestAnimationFrame = function(a, b, c) {
                "undefined" == typeof c && (c = {
                    data: {
                        last_frame: 0
                    }
                });
                var d = (new Date).getTime(),
                    e = Math.max(0, 16 - (d - c.data.last_frame)),
                    f = window.top.setTimeout(function() {
                        a(d + e)
                    }, e);
                return c.data.last_frame = d + e, f
            }, window.top.cancelAnimationFrame = function(a) {
                clearTimeout(a)
            })
        }();
    var o = function(a, b) {
        this.element = a, this.container, this.listeners = null, this.data = {
            paused: !1,
            last_frame: 0,
            animation_frame: null,
            timer: !1,
            total_duration: null,
            prev_time: null,
            drawn_units: [],
            text_elements: {
                Days: null,
                Hours: null,
                Minutes: null,
                Seconds: null
            },
            attributes: {
                canvas: null,
                context: null,
                item_size: null,
                line_width: null,
                radius: null,
                outer_radius: null
            },
            state: {
                fading: {
                    Days: !1,
                    Hours: !1,
                    Minutes: !1,
                    Seconds: !1
                }
            }
        }, this.config = null, this.setOptions(b), this.initialize()
    };
    o.prototype.initialize = function(c) {
        this.data.drawn_units = [];
        for (var d in this.config.time) this.config.time[d].show && this.data.drawn_units.push(d);
        a(this.element).children("div.time_circles").remove(), "undefined" == typeof c && (c = !0), (c || null === this.listeners) && (this.listeners = {
            all: [],
            visible: []
        }), this.container = a("<div>"), this.container.addClass("time_circles"), this.container.appendTo(this.element), this.data.attributes.canvas = a("<canvas>");
        try {
            this.data.attributes.context = this.data.attributes.canvas[0].getContext("2d")
        } catch (a) {
            b = !0
        }
        var e = this.element.offsetHeight,
            f = this.element.offsetWidth;
        0 === e && (e = a(this.element).height()), 0 === f && (f = a(this.element).width()), 0 === e && f > 0 ? e = f / this.data.drawn_units.length : 0 === f && e > 0 && (f = e * this.data.drawn_units.length), this.data.attributes.canvas[0].height = e, this.data.attributes.canvas[0].width = f, this.data.attributes.canvas.appendTo(this.container), this.data.attributes.item_size = Math.min(this.data.attributes.canvas[0].width / this.data.drawn_units.length, this.data.attributes.canvas[0].height), this.data.attributes.line_width = this.data.attributes.item_size * this.config.fg_width, this.data.attributes.radius = (.8 * this.data.attributes.item_size - this.data.attributes.line_width) / 2, this.data.attributes.outer_radius = this.data.attributes.radius + .5 * Math.max(this.data.attributes.line_width, this.data.attributes.line_width * this.config.bg_width);
        var g = 0;
        for (var h in this.data.text_elements)
            if (this.config.time[h].show) {
                var i = a("<div>");
                i.addClass("textDiv_" + h), i.css("top", Math.round(.35 * this.data.attributes.item_size)), i.css("left", Math.round(g++ * this.data.attributes.item_size)), i.css("width", this.data.attributes.item_size), i.appendTo(this.container);
                var j = a("<span>");
                j.appendTo(i);
                var k = a("<h4>");
                k.text(this.config.time[h].text), k.appendTo(i), this.data.text_elements[h] = j
            }
        this.config.start && this.data.paused === !1 && this.start()
    }, o.prototype.update = function() {
        var a, b, d = this.data.prev_time,
            e = new Date;
        if (this.data.prev_time = e, null === d && (d = e), !this.config.count_past_zero && e > this.data.attributes.ref_date) {
            for (var g in this.data.drawn_units) {
                var i = this.data.drawn_units[g];
                this.data.text_elements[i].text("0");
                var j = g * this.data.attributes.item_size + this.data.attributes.item_size / 2,
                    k = this.data.attributes.item_size / 2,
                    l = this.config.time[i].color;
                this.drawArc(j, k, l, 0)
            }
            return void this.stop()
        }
        a = (this.data.attributes.ref_date - e) / 1e3, b = (this.data.attributes.ref_date - d) / 1e3;
        var n = "smooth" !== this.config.animation,
            o = m(a, b, this.data.total_duration, this.data.drawn_units, n),
            p = m(a, b, h.Years, f, n),
            g = 0,
            q = 0,
            r = null,
            s = this.data.drawn_units.slice();
        for (var g in f) {
            var i = f[g];
            if (Math.floor(p.raw_time[i]) !== Math.floor(p.raw_old_time[i]) && this.notifyListeners(i, Math.floor(p.time[i]), Math.floor(a), "all"), !(s.indexOf(i) < 0)) {
                Math.floor(o.raw_time[i]) !== Math.floor(o.raw_old_time[i]) && this.notifyListeners(i, Math.floor(o.time[i]), Math.floor(a), "visible"), this.data.text_elements[i].text(Math.floor(Math.abs(o.time[i])));
                var j = q * this.data.attributes.item_size + this.data.attributes.item_size / 2,
                    k = this.data.attributes.item_size / 2,
                    l = this.config.time[i].color;
                "smooth" === this.config.animation ? (null !== r && (Math.floor(o.time[r]) > Math.floor(o.old_time[r]) ? (this.radialFade(j, k, l, 1, i), this.data.state.fading[i] = !0) : Math.floor(o.time[r]) < Math.floor(o.old_time[r]) && (this.radialFade(j, k, l, 0, i), this.data.state.fading[i] = !0)), this.data.state.fading[i] || this.drawArc(j, k, l, o.pct[i])) : this.animateArc(j, k, l, o.pct[i], o.old_pct[i], (new Date).getTime() + c), r = i, q++
            }
        }
        var t = this,
            u = function() {
                t.update.call(t)
            };
        if ("smooth" === this.config.animation) this.data.animation_frame = window.top.requestAnimationFrame(u, t.element, t);
        else {
            var v = a % 1 * 1e3;
            v < 0 && (v = 1e3 + v), v += 50, t.data.animation_frame = window.top.setTimeout(function() {
                t.data.animation_frame = window.top.requestAnimationFrame(u, t.element, t)
            }, v)
        }
    }, o.prototype.animateArc = function(a, d, e, f, g, h) {
        if (!b) {
            var i = g - f;
            if (Math.abs(i) > .5) 0 === f ? this.radialFade(a, d, e, 1) : this.radialFade(a, d, e, 0);
            else {
                var j = (c - (h - (new Date).getTime())) / c;
                j > 1 && (j = 1);
                var k = g * (1 - j) + f * j;
                if (this.drawArc(a, d, e, k), j >= 1) return;
                var l = this;
                window.top.requestAnimationFrame(function() {
                    l.animateArc(a, d, e, f, g, h)
                }, this.element, null)
            }
        }
    }, o.prototype.drawArc = function(a, c, d, e) {
        if (!b) {
            var f = Math.max(this.data.attributes.outer_radius, this.data.attributes.item_size / 2);
            this.data.attributes.context.clearRect(a - f, c - f, 2 * f, 2 * f), this.config.use_background && (this.data.attributes.context.beginPath(), this.data.attributes.context.arc(a, c, this.data.attributes.radius, 0, 2 * Math.PI, !1), this.data.attributes.context.lineWidth = this.data.attributes.line_width * this.config.bg_width, this.data.attributes.context.strokeStyle = this.config.circle_bg_color, this.data.attributes.context.stroke());
            var g, h, i, j = -.5 * Math.PI,
                k = 2 * Math.PI;
            g = j + this.config.start_angle / 360 * k;
            var l = 2 * e * Math.PI;
            "Both" === this.config.direction ? (i = !1, g -= l / 2, h = g + l) : "Clockwise" === this.config.direction ? (i = !1, h = g + l) : (i = !0, h = g - l), this.data.attributes.context.beginPath(), this.data.attributes.context.arc(a, c, this.data.attributes.radius, g, h, i), this.data.attributes.context.lineWidth = this.data.attributes.line_width, this.data.attributes.context.strokeStyle = d, this.data.attributes.context.stroke()
        }
    }, o.prototype.radialFade = function(a, b, c, d, e) {
        var j, f = i(c),
            g = this,
            h = .2 * (1 === d ? -1 : 1);
        for (j = 0; d <= 1 && d >= 0; j++) ! function() {
            var c = 50 * j,
                e = "rgba(" + f.r + ", " + f.g + ", " + f.b + ", " + Math.round(10 * d) / 10 + ")";
            window.top.setTimeout(function() {
                g.drawArc(a, b, e, 1)
            }, c)
        }(), d += h;
        void 0 !== typeof e && window.top.setTimeout(function() {
            g.data.state.fading[e] = !1
        }, 50 * j)
    }, o.prototype.timeLeft = function() {
        var a = new Date;
        return (this.data.attributes.ref_date - a) / 1e3
    }, o.prototype.start = function() {
        window.top.cancelAnimationFrame(this.data.animation_frame), window.top.clearTimeout(this.data.animation_frame);
        var b = a(this.element).data("date");
        if ("undefined" == typeof b && (b = a(this.element).attr("data-date")), "string" == typeof b) this.data.attributes.ref_date = l(b);
        else if ("number" == typeof this.data.timer) this.data.paused && (this.data.attributes.ref_date = (new Date).getTime() + 1e3 * this.data.timer);
        else {
            var c = a(this.element).data("timer");
            "undefined" == typeof c && (c = a(this.element).attr("data-timer")), "string" == typeof c && (c = parseFloat(c)), "number" == typeof c ? (this.data.timer = c, this.data.attributes.ref_date = (new Date).getTime() + 1e3 * c) : this.data.attributes.ref_date = this.config.ref_date
        }
        this.data.paused = !1, this.update()
    }, o.prototype.restart = function() {
        this.data.timer = !1, this.start()
    }, o.prototype.stop = function() {
        "number" == typeof this.data.timer && (this.data.timer = this.timeLeft(this)), this.data.paused = !0, window.top.cancelAnimationFrame(this.data.animation_frame)
    }, o.prototype.destroy = function() {
        this.stop(), this.container.remove(), a(this.element).removeAttr("data-tc-id"), a(this.element).removeData("tc-id")
    }, o.prototype.setOptions = function(b) {
        if (null === this.config && (this.default_options.ref_date = new Date, this.config = a.extend(!0, {}, this.default_options)), a.extend(!0, this.config, b), this.data.total_duration = this.config.total_duration, "string" == typeof this.data.total_duration)
            if ("undefined" != typeof h[this.data.total_duration]) this.data.total_duration = h[this.data.total_duration];
            else if ("Auto" === this.data.total_duration) {
            for (var c in this.config.time)
                if (this.config.time[c].show) {
                    this.data.total_duration = h[g[c]];
                    break
                }
        } else this.data.total_duration = h.Years, console.error("Valid values for TimeCircles config.total_duration are either numeric, or (string) Years, Months, Days, Hours, Minutes, Auto")
    }, o.prototype.addListener = function(a, b, c) {
        "function" == typeof a && ("undefined" == typeof c && (c = "visible"), this.listeners[c].push({
            func: a,
            scope: b
        }))
    }, o.prototype.notifyListeners = function(a, b, c, d) {
        for (var e = 0; e < this.listeners[d].length; e++) {
            var f = this.listeners[d][e];
            f.func.apply(f.scope, [a, b, c])
        }
    }, o.prototype.default_options = {
        ref_date: new Date,
        start: !0,
        animation: "smooth",
        count_past_zero: !0,
        circle_bg_color: "#60686F",
        use_background: !0,
        fg_width: .1,
        bg_width: 1.2,
        total_duration: "Auto",
        direction: "Clockwise",
        start_angle: 0,
        time: {
            Days: {
                show: !0,
                text: "Days",
                color: "#FC6"
            },
            Hours: {
                show: !0,
                text: "Hours",
                color: "#9CF"
            },
            Minutes: {
                show: !0,
                text: "Minutes",
                color: "#BFB"
            },
            Seconds: {
                show: !0,
                text: "Seconds",
                color: "#F99"
            }
        }
    };
    var p = function(a, b) {
        this.elements = a, this.options = b, this.foreach()
    };
    p.prototype.getInstance = function(b) {
        var c, d = a(b).data("tc-id");
        if ("undefined" == typeof d && (d = k(), a(b).attr("data-tc-id", d)), "undefined" == typeof n[d]) {
            var e = this.options,
                f = a(b).data("options");
            "string" == typeof f && (f = JSON.parse(f)), "object" == typeof f && (e = a.extend(!0, {}, this.options, f)), c = new o(b, e), n[d] = c
        } else c = n[d], "undefined" != typeof this.options && c.setOptions(this.options);
        return c
    }, p.prototype.foreach = function(a) {
        var b = this;
        return this.elements.each(function() {
            var c = b.getInstance(this);
            "function" == typeof a && a(c)
        }), this
    }, p.prototype.start = function() {
        return this.foreach(function(a) {
            a.start()
        }), this
    }, p.prototype.stop = function() {
        return this.foreach(function(a) {
            a.stop()
        }), this
    }, p.prototype.restart = function() {
        return this.foreach(function(a) {
            a.restart()
        }), this
    }, p.prototype.rebuild = function() {
        return this.foreach(function(a) {
            a.initialize(!1)
        }), this
    }, p.prototype.getTime = function() {
        return this.getInstance(this.elements[0]).timeLeft()
    }, p.prototype.addListener = function(a, b) {
        "undefined" == typeof b && (b = "visible");
        var c = this;
        return this.foreach(function(d) {
            d.addListener(a, c.elements, b)
        }), this
    }, p.prototype.destroy = function() {
        return this.foreach(function(a) {
            a.destroy()
        }), this
    }, p.prototype.end = function() {
        return this.elements
    }, a.fn.TimeCircles = function(a) {
        return new p(this, a)
    }
}(jQuery);