def wrap(v,vmin,vmax):
    p=vmax-vmin
    return (v-vmin)%p+vmin