"""power_size.py — how much power, cooling and space Maestro-1 needs.

Gopala rents rather than builds, but he still has to know these numbers:
they decide which data halls can take his cluster at all, and they are
a line on every invoice that passes through power.
"""
NODES = 128                 # 1,024 GPUs, 8 per node
NODE_MAX_KW = 10.2          # DGX H100 maximum system power (NVIDIA user guide)
NODE_TYPICAL = 0.80         # our assumption: sustained draw ~80% of max in training
NET_STORAGE_KW = 0.12       # our assumption: switches, storage, management = +12% of IT
PUE = {"modern liquid-assisted hall": 1.25, "2025 global average": 1.54}
PRICE_KWH = 0.08            # our assumption, $ per kWh
RACK_LIMITS_KW = [15, 40, 130]   # legacy, air-cooled AI-ready, liquid (GB200 NVL72 class)

def main():
    it_max = NODES * NODE_MAX_KW * (1 + NET_STORAGE_KW)
    it_avg = NODES * NODE_MAX_KW * NODE_TYPICAL * (1 + NET_STORAGE_KW)
    print(f"IT load: {it_max/1000:.2f} MW design (max), {it_avg/1000:.2f} MW typical")
    for name, pue in PUE.items():
        fac = it_avg * pue
        mwh = fac * 730 / 1000
        print(f"  {name:28s} PUE {pue:.2f}: facility {fac/1000:.2f} MW, "
              f"{mwh:,.0f} MWh/month, ${mwh*1000*PRICE_KWH/1e3:,.0f}k/month")
    print("racks needed:")
    for lim in RACK_LIMITS_KW:
        per = int(lim // NODE_MAX_KW)
        if per == 0:
            print(f"  {lim:3d} kW racks: cannot hold one node"); continue
        racks = -(-NODES // per)
        print(f"  {lim:3d} kW racks: {per} nodes/rack -> {racks} racks")
    heat_btu = it_avg * 3412
    print(f"heat to remove: {it_avg:,.0f} kW = {heat_btu/12000:,.0f} tons of cooling")
    gpu_kw = NODES * 8 * 0.7
    print(f"GPUs alone at 700 W TDP: {gpu_kw:.0f} kW "
          f"({gpu_kw/(NODES*NODE_MAX_KW):.0%} of node max)")

if __name__ == "__main__":
    main()
