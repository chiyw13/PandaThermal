import pytest
import pandathermal as pth


@pytest.fixture()
def fix_create():
    g = pth.create_empty_directed_network()

    pth.add_srce(g, "SRCE")

    pth.add_sink(g, "SNK1", p_kw=10.0)
    pth.add_sink(g, "SNK2", p_kw=20.0)
    pth.add_sink(g, "SNK3", p_kw=10.0)
    pth.add_sink(g, "SNK4", p_kw=50.0)
    pth.add_sink(g, "SNK5", p_kw=10.0)
    pth.add_sink(g, "SNK6", p_kw=20.0)
    pth.add_sink(g, "SNK7", p_kw=10.0)
    pth.add_sink(g, "SNK8", p_kw=30.0)
    pth.add_sink(g, "SNK9", p_kw=10.0)

    pth.add_nodes_from(g, ["N{}".format(i) for i in range(7)])

    edges = [
        ("SRCE", "N0"),
        ("N0", "SNK1"),
        ("N1", "SNK2"),
        ("N2", "SNK3"),
        ("N2", "SNK4"),
        ("N2", "SNK5"),
        ("N3", "SNK6"),
        ("N4", "SNK7"),
        ("N5", "SNK8"),
        ("N6", "SNK9"),
        ("N0", "N1"),
        ("N1", "N2"),
        ("N2", "N3"),
        ("N3", "N4"),
        ("N4", "N5"),
        ("N5", "N6"),
    ]
    pth.add_pipes_from(g, edges)

    return g


def test_compute_pipes_diameter(fix_create):
    g = fix_create
    waited = {
        ("SRCE", "N0"): 0.72,
        ("N0", "SNK1"): 0.17,
        ("N0", "N1"): 0.7,
        ("N1", "SNK2"): 0.25,
        ("N1", "N2"): 0.65,
        ("N2", "SNK3"): 0.17,
        ("N2", "SNK4"): 0.39,
        ("N2", "SNK5"): 0.17,
        ("N2", "N3"): 0.46,
        ("N3", "SNK6"): 0.25,
        ("N3", "N4"): 0.39,
        ("N4", "SNK7"): 0.17,
        ("N4", "N5"): 0.35,
        ("N5", "SNK8"): 0.3,
        ("N5", "N6"): 0.17,
        ("N6", "SNK9"): 0.17,
    }
    assert pth.compute_pipes_diameter(g, dt=40) == waited


def test_compute_pipes_max_m_dot(fix_create):
    g = fix_create
    waited = {
        ("SRCE", "N0"): 0.81,
        ("N0", "SNK1"): 0.05,
        ("N0", "N1"): 0.76,
        ("N1", "SNK2"): 0.1,
        ("N1", "N2"): 0.67,
        ("N2", "SNK3"): 0.05,
        ("N2", "SNK4"): 0.24,
        ("N2", "SNK5"): 0.05,
        ("N2", "N3"): 0.33,
        ("N3", "SNK6"): 0.1,
        ("N3", "N4"): 0.24,
        ("N4", "SNK7"): 0.05,
        ("N4", "N5"): 0.19,
        ("N5", "SNK8"): 0.14,
        ("N5", "N6"): 0.05,
        ("N6", "SNK9"): 0.05,
    }
    assert pth.compute_pipes_max_m_dot(g, dt=40) == waited


def test_lmtd():
    t_i_src = 80.0
    t_o_src = 50.0
    t_i_snk = 20.0
    t_o_snk = 40.0
    assert round(pth.lmtd(t_i_src, t_o_src, t_i_snk, t_o_snk), 2) == 34.76


def test_hex_surf():
    assert round(pth.hex_surf(20.0, 34.76), 2) == 0.58
