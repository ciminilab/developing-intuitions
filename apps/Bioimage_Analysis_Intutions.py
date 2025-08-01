import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells

    #TODO - check that the spinner works when running remote micropip installs, if not maybe see if will work outside the setup cell

    import marimo as mo

    __generated_with = "0.13.11"

    with mo.status.spinner(title="Installing and importing packages") as _spinner:
        import os
        import numpy
        import skimage
        import wigglystuff
        _spinner.update()


@app.class_definition(hide_code=True)
#TODO - can we figure out how to set a max cache length, without trying to subclass dict ? Couldn't figure it out in ~30 minutes, but would be nice to have. Otherwise, should at least see if we can make cache clearable (same with named cache).

class ProcessedImage:
    def __init__(self,im,gt=False):
        self.raw = im
        self.im = im
        self.gt = gt
        self.disp_image = False
        self.cache = {} 
        self.named_cache = {}

    def return_raw(self):
        return self.raw

    def im(self):
        return self.im

    def blur(self,diam=False):
        if not diam:
            diam = 10
        return skimage.filters.gaussian(self.im,sigma=diam)

    def roll_ball(self,diam=False):
        if not diam:
            diam = 100
        return self.im-(skimage.restoration.rolling_ball(self.im,radius=diam/2))

    def power_transform(self,exp_to_use=False):
        import numpy
        if not exp_to_use:
            exp_to_use=1
        if exp_to_use <1:
            im = numpy.where(self.im==0,0.00000001,self.im)
        else:
            im = self.im
        return im**(exp_to_use)

    def invert(self):
        return skimage.util.invert(self.im)

    def sato(self,sigma=False):
        if not sigma:
            sigmas = range(3,8,1)
        else:
            sigmas = range(int(sigma)-2,int(sigma)+3,1)
        return skimage.filters.sato(self.im,sigmas=sigmas,black_ridges=False)

    def texture_transform(self,sigma=False):
        if not sigma:
            sigma = 5
        img_mean = skimage.filters.gaussian(self.im, sigma, mode="constant")
        img_squared =  skimage.filters.gaussian(self.im ** 2, sigma, mode="constant")
        return img_squared - img_mean ** 2

    def tophat(self,diam=False):
        if not diam:
            diam = 5
        return skimage.morphology.white_tophat(self.im,footprint=skimage.morphology.disk(diam/2))

    def set_named_cache(self, name):
        #Probably do a check that the name isn't "current" (if we don't want user to have to save all things going to math)
        #Could also maybe use it if we want to be able to add custom intermediates to the display box - will ponder when we get there
        self.named_cache[name] = self.im
        return self.im

    def get_named_image(self,name):
        if name.lower() == '"current"':
            return self.im
        else:
            if name not in self.named_cache.keys():
                print(f"You have an undefined name in your list; {name} cannot be easily mapped to any of the following: {", ".join(self.named_cache.keys())}. Please check spelling and try again")
            return self.named_cache[name]

    def subtract(self,im1name,val_or_im2name):
        if type(val_or_im2name) != float:
            val_or_im2name = self.get_named_image(val_or_im2name)
        return self.get_named_image(im1name) - val_or_im2name

    def add(self,im1name,val_or_im2name):
        pass

    def divide(self,im1name,val_or_im2name):
        pass

    def multiply(self,im1name,val_or_im2name):
        pass

    def clip(self):
        pass

    def threshold_li(self,min=0,max=1,corr_factor=1):
        """
        Make sure this gets into the help text somewhere:
            *Note that for functions with multiple parameters, you can pass all, none, or some, but if some, they must be in order; so if you want to change the 3rd parameter, you have to leave the first two there with their default parameters*
        """
        pass

    def threshold_otsu(self,min=0,max=1,corr_factor=1,classes=2,keep_top=1):
        pass

    def label(self):
        pass

    def measure(self):
        pass

    def score(self):
        pass

    def distance_tranform(self):
        pass

    def fill_holes(self,diam=False):
        pass

    def erode(self,diam=False):
        pass

    def dilate(self,diam=False):
        pass

    def open(self,diam=False):
        pass

    def close(self,diam=False):
        pass

    def test_for_numeric(self,param):
        #This is gross but isnumeric barfs on decimals, which is insane
        try:
            return float(param.strip())
        except:
            return param.strip()

    def parse_vals(self,value_list):
        self.im = self.raw
        current_processing_state=""
        defined_funcs = {
            'blur':self.blur, 'rollingball':self.roll_ball, 'powertransform':self.power_transform,
            'invert':self.invert, 'tophat':self.tophat, 'ridge':self.sato,
            'savelaststepas':self.set_named_cache, 'subtract':self.subtract, 'raw':self.return_raw, 'texturetransform':self.texture_transform}
        for val in value_list:
            if "(" in val:
                userfunc, userargstring = val.split("(")
                userargs= [self.test_for_numeric(x) for x in userargstring.split(")")[0].split(",")]
            else:
                userfunc=val
                userargs=False
            parseduserfunc = userfunc.lower().replace(" ","")
            if parseduserfunc not in defined_funcs.keys(): #TODO later: fuzzy matching (but this is fine for now)
                print(f"You have an undefined function in your list; {userfunc} cannot be easily mapped to any of the following: {", ".join(defined_funcs.keys())}. Please check spelling and try again")
                return(self.im)
            else:
                func = defined_funcs[parseduserfunc]
            if not userargs:
                current_processing_state+=f"{parseduserfunc};"
                if current_processing_state not in self.cache.keys():
                    self.im = func()
                    self.cache[current_processing_state] = self.im
                else:
                    self.im = self.cache[current_processing_state] 
            else:
                current_processing_state+=f"{parseduserfunc}({','.join([str(x) for x in userargs])});"
                if current_processing_state not in self.cache.keys():
                    self.im = func(*userargs)
                    self.cache[current_processing_state] = self.im
                else:
                    self.im = self.cache[current_processing_state] 

        return self.im


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    #Lesson 1 - Filters of Many Flavors (Making sure the thing I care about is bright, and everything else is dark)
    ## Let's Start With A Raw Image

    All these images come from the `skimage.data` library - see that library for more information on any image!
    """
    )
    return


@app.cell(hide_code=True)
def _():
    #TODO - maybe have a crop button
    def load_image(imdesc):
        data_dir = "images/data/"
        loaded_image = skimage.io.imread(os.path.join(mo.notebook_location(), data_dir,imdesc["name"]))
        if imdesc["3D_slice"]:
            loaded_image = skimage.util.img_as_float(loaded_image[imdesc["3D_slice"],:,:])
        if imdesc["hist_deconvolve"]:
            loaded_image = skimage.color.rgb2hed(loaded_image)[:,:,2]
            loaded_image = skimage.util.img_as_float(skimage.exposure.rescale_intensity(loaded_image, in_range = (0, numpy.percentile(loaded_image,99))))
        if imdesc["4D"]:
            loaded_image = skimage.util.img_as_float(loaded_image[14,1,:,:])
        if imdesc["orig_color"]:
            loaded_image = skimage.util.img_as_float(skimage.color.rgb2gray(loaded_image))
        return loaded_image

    test_images = {
        "Brain Slice":{"name":"brain.tiff","orig_color":False,"hist_deconvolve":False,"3D_slice":5, "4D":False},
        "Bricks":{"name":"brick.png","orig_color":False,"hist_deconvolve":False,"3D_slice":False, "4D":False},
        "Hubble Deep Field":{"name":"hubble_deep_field.jpg","orig_color":True,"hist_deconvolve":False,"3D_slice":False, "4D":False}, 
        "Human Nuclei":{"name":"mitosis.tif","orig_color":False,"hist_deconvolve":False,"3D_slice":False, "4D":False},
        "Kidney Cells": {"name":"ihc.png","orig_color":False,"hist_deconvolve":True,"3D_slice":False, "4D":False}, 
        "Moon Surface":{"name":"moon.png","orig_color":False,"hist_deconvolve":False,"3D_slice":False, "4D":False},
        "Nuclear Envelope": {"name":"protein_transport.tif","orig_color":False,"hist_deconvolve":False,"3D_slice":False, "4D":True}, 
        "Pompeii Coins":{"name":"coins.png","orig_color":False,"hist_deconvolve":False,"3D_slice":False, "4D":False},


    }

    im_choice = mo.ui.dropdown(label="Pick an image to use",options=test_images.keys(),value="Human Nuclei")
    im_choice
    return im_choice, load_image, test_images


@app.cell
def _(im_choice, load_image, test_images):
    image = load_image(test_images[im_choice.value])
    processed_image = ProcessedImage(image)
    mo.image(processed_image.raw)
    return (processed_image,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ## What shall we do to it?

    Pass one or more implemented operations into the list (_try literally cutting and pasting them!_), and see how your output image changes! 

    Some operations may be slow (especially if you make them very different than the listed default value); you must wait for the current process to be finish to adjust options in the list, and the whole pipeline runs every time. This is somewhat accelerated by caching all the intermediates; future improvements may be to turn caching off (or limit cache length or have a "clear cache button") and the ability to turn on-the-fly processing on and off, author time permitting.

    Currently implemented operations are listed below - some contain optional parameters that you may (or may not) wish to play with. IE for `Blur`, you can pass `Blur (20)` or `Blur(2)`; you can also just pass `Blur` and it will try to use a reasonable default. More operations (and links to more detailed help) coming soon!
    """
    )
    return


@app.cell(hide_code=True)
def _():
    lesson_1_funcs = r"""
    * Blur(10)
        * *Gaussian Blur; Number in parentheses equals: diameter (in pixels) of the smoothing kernel sigma*
    * Rolling Ball(100)
        * *Rolling ball background subtraction; Number in parentheses equals: diameter (in pixels) of the ball to be rolled*
    * Invert
        * *Invert the image (best for grayscale, or after something like ridge enhancement*
    * PowerTranform(1)
        * *Multiply the image by an exponent - an exponent value of >1 will make the brightest and dimmest pixel be proportionately farther from each other (but all at lower absolute numbers); conversely, an exponent of <1 will decrease the fold-change between foreground and background but will make the numbers higher. A value of 1 will do nothing!*
    * Tophat(5)
        * *Enhance round-ish things of the diameter passed in - remove anything larger than that diameter, approximately.*
    * Ridge(5)
        * *Enhance anything vaguely tube-like*
    * TextureTransform(5)
        * *Enhance areas with textures of a particular size. See how it performs on an inverted (vs not) image!*
    """
    mo.md(lesson_1_funcs)
    return (lesson_1_funcs,)


@app.cell
def _():
    mo.md(r"""## Let's get filtering!""")
    return


@app.cell(hide_code=True)
def _():
    imfunctions = mo.ui.anywidget(
        wigglystuff.SortableList(
            [
                "Blur(2)",
                "Rolling Ball(50)"
            ],addable=True, removable=True, editable=True
        )
    )

    imfunctions

    #TODO - maybe also add switch/button for "update image live", if this becomes slow
    #TODO - also maybe a clear cache button, if eventually figure that out
    #TODO - "Clear all" button
    #TODO - "Generate Suggested" button (once we can add a few different images)
    return (imfunctions,)


@app.cell
def _():
    mo.md(
        r"""
    ## Behold, a Processed Image!

    **How close did you get to "the thing I care about is bright, and everything else is dark?"**
    """
    )
    return


@app.cell(hide_code=True)
def _(imfunctions, processed_image):
    #TODO - make it so you could show any named intermediates also/instead (but default to just the end of the workflow)

    processed_image.parse_vals(imfunctions.value["value"])

    mo.image(processed_image.im)
    return


@app.cell
def _():
    mo.md(r"""# Lesson 2 (Optional) - Filter It, Then Filter It Again (When one round of filtering is not getting it done)""")
    return


@app.cell
def _():
    mo.md(r"""### What If We Want to Do Two Kinds of Filtering""")
    return


@app.cell
def _():
    lesson_2_funcs = r"""
    **These functions are designed for letting you go down one or more "paths" (maybe blurring in one and then speckle enhancing in another) and then doing math between outputs (or the original loaded image). They're incredibly handy once you're comfortable, but don't need to be part of your initial thinking!**

    * Raw
        * *Return to the loaded raw image*
    * Save Last Step As("somename")
        * *Save the last step with a distinct name so that you can do mathematical operations. The name must be in quotes (so `SaveLastStepAs("A")` is fine but `SaveLastStepAs(B)` is not. Do not use numbers as the names (`Image2` is fine, but `2` is not) or  the literal name "Current".
    * Subtract(A,B) 
        * *Subtract a second image OR a number from the first image (so `Subtract("Current","A")` and `Subtract("B",0.3)` are fine; `Subtract(0.3,"B")` is not (there's really never a reason to do that). `Current` will let you use the current image without using a Save Last Step As*
        """
    mo.md(lesson_2_funcs)
    return


@app.cell(hide_code=True)
def _(lesson_1_funcs):

    mo.accordion({"### Reminder of your original functions":lesson_1_funcs})
    return


@app.cell
def _():
    mo.md(r"""## Let's get filtering (again)!""")
    return


@app.cell
def _():
    mo.md(r"""# Lesson 3 - Stuff vs Not Stuff (Thresholding)""")
    return


@app.cell
def _():
    #TODO - fancy view visualization (raw, processed, labels/outlines, stats)
    #TODOAFTER - accuracy visualization
    return


@app.cell
def _():
    mo.md(r"""# Lesson 4 - Not Just Stuff but The Right Stuff (Tweaking your segmentations)""")
    return


if __name__ == "__main__":
    app.run()
